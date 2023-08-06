# -*- coding: utf-8 -*-

from typing import Any, Dict

from kiara import KiaraModule
from kiara.exceptions import KiaraProcessingException
from kiara.models.module import KiaraModuleConfig
from kiara.models.values.value import ValueMap
from kiara.modules import ValueSetSchema
from kiara_plugin.tabular.models.table import KiaraArray
from pydantic import Field


def get_stopwords():

    # TODO: make that smarter
    pass

    import nltk

    nltk.download("punkt")
    nltk.download("stopwords")
    from nltk.corpus import stopwords

    return stopwords


class TokenizeTextConfig(KiaraModuleConfig):

    filter_non_alpha: bool = Field(
        description="Whether to filter out non alpha tokens.", default=True
    )
    min_token_length: int = Field(description="The minimum token length.", default=3)
    to_lowercase: bool = Field(
        description="Whether to lowercase the tokens.", default=True
    )


class TokenizeTextModule(KiaraModule):
    """Tokenize a string."""

    _config_cls = TokenizeTextConfig
    _module_type_name = "tokenize.string"

    def create_inputs_schema(
        self,
    ) -> ValueSetSchema:

        inputs = {"text": {"type": "string", "doc": "The text to tokenize."}}

        return inputs

    def create_outputs_schema(
        self,
    ) -> ValueSetSchema:

        outputs = {
            "token_list": {
                "type": "list",
                "doc": "The tokenized version of the input text.",
            }
        }
        return outputs

    def process(self, inputs: ValueMap, outputs: ValueMap) -> None:

        import nltk

        # TODO: module-independent caching?
        # language = inputs.get_value_data("language")
        #
        text = inputs.get_value_data("text")
        tokenized = nltk.word_tokenize(text)

        result = tokenized
        if self.get_config_value("min_token_length") > 0:
            result = (
                x
                for x in tokenized
                if len(x) >= self.get_config_value("min_token_length")
            )

        if self.get_config_value("filter_non_alpha"):
            result = (x for x in result if x.isalpha())

        if self.get_config_value("to_lowercase"):
            result = (x.lower() for x in result)

        outputs.set_value("token_list", list(result))


class TokenizTextArrayeModule(KiaraModule):
    """Split sentences into words or words into characters.
    In other words, this operation establishes the word boundaries (i.e., tokens) a very helpful way of finding patterns. It is also the typical step prior to stemming and lemmatization
    """

    _module_type_name = "tokenize.texts_array"

    KIARA_METADATA = {
        "tags": ["tokenize", "tokens"],
    }

    def create_inputs_schema(
        self,
    ) -> ValueSetSchema:

        return {
            "texts_array": {
                "type": "array",
                "doc": "An array of text items to be tokenized.",
            },
            "tokenize_by_word": {
                "type": "boolean",
                "doc": "Whether to tokenize by word (default), or character.",
                "default": True,
            },
        }

    def create_outputs_schema(
        self,
    ) -> ValueSetSchema:

        return {
            "tokens_array": {
                "type": "array",
                "doc": "The tokenized content, as an array of lists of strings.",
            }
        }

    def process(self, inputs: ValueMap, outputs: ValueMap):

        import warnings

        import nltk
        import numpy as np
        import pyarrow as pa
        import vaex

        array: KiaraArray = inputs.get_value_data("texts_array")
        # tokenize_by_word: bool = inputs.get_value_data("tokenize_by_word")

        column: pa.Array = array.arrow_array

        warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)

        def word_tokenize(word):
            result = nltk.word_tokenize(word)
            return result

        df = vaex.from_arrays(column=column)

        tokenized = df.apply(word_tokenize, arguments=[df.column])

        result_array = tokenized.to_arrow(convert_to_native=True)
        # TODO: remove this cast once the array data type can handle non-chunked arrays
        chunked = pa.chunked_array(result_array)
        outputs.set_values(tokens_array=chunked)

        # pandas_series: Series = column.to_pandas()
        #
        # tokenized = pandas_series.apply(lambda x: nltk.word_tokenize(x))
        #
        # result_array = pa.Array.from_pandas(tokenized)
        #
        # outputs.set_values(tokens_array=result_array)


class RemoveStopwordsModule(KiaraModule):
    """Remove stopwords from an array of token-lists."""

    _module_type_name = "remove_stopwords.from.tokens_array"

    def create_inputs_schema(
        self,
    ) -> ValueSetSchema:

        # TODO: do something smart and check whether languages are already downloaded, if so, display selection in doc
        inputs: Dict[str, Dict[str, Any]] = {
            "tokens_array": {
                "type": "array",
                "doc": "An array of string lists (a list of tokens).",
            },
            "languages": {
                "type": "list",
                # "doc": f"A list of language names to use default stopword lists for. Available: {', '.join(get_stopwords().fileids())}.",
                "doc": "A list of language names to use default stopword lists for.",
                "optional": True,
            },
            "additional_stopwords": {
                "type": "list",
                "doc": "A list of additional, custom stopwords.",
                "optional": True,
            },
        }
        return inputs

    def create_outputs_schema(
        self,
    ) -> ValueSetSchema:

        outputs = {
            "token_list": {
                "type": "array",
                "doc": "An array of string lists, with the stopwords removed.",
            }
        }
        return outputs

    def process(self, inputs: ValueMap, outputs: ValueMap) -> None:

        import pyarrow as pa

        custom_stopwords = inputs.get_value_data("additional_stopwords")
        languages = inputs.get_value_data("languages")
        if isinstance(languages, str):
            languages = [languages]

        stopwords = set()
        if languages:
            for language in languages:
                if language not in get_stopwords().fileids():
                    raise KiaraProcessingException(
                        f"Invalid language: {language}. Available: {', '.join(get_stopwords().fileids())}."
                    )
                stopwords.update(get_stopwords().words(language))

        if custom_stopwords:
            stopwords.update(custom_stopwords)

        if not stopwords:
            outputs.set_value("token_list", inputs.get_value_obj("token_lists"))
            return

        token_lists = inputs.get_value_data("token_lists")

        if hasattr(token_lists, "to_pylist"):
            token_lists = token_lists.to_pylist()

        result = []
        for token_list in token_lists:

            cleaned_list = [x for x in token_list if x not in stopwords]
            result.append(cleaned_list)

        outputs.set_value("token_list", pa.array(result))
