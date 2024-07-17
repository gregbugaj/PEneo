"""

A mapping of the supported VIE backbone,
with the corresponding model, configuration, and processor utils.


"""

from dataclasses import dataclass
from typing import Callable, List, Optional, Union

from transformers import (
    ImageProcessingMixin,
    PretrainedConfig,
    PreTrainedModel,
    PreTrainedTokenizerBase,
    ProcessorMixin,
)
from transformers.models.layoutlmv2 import (
    LayoutLMv2Config,
    LayoutLMv2ImageProcessor,
    LayoutLMv2Model,
    LayoutLMv2Processor,
)
from transformers.models.layoutlmv3 import LayoutLMv3ImageProcessor
from transformers.models.layoutxlm import LayoutXLMProcessor, LayoutXLMTokenizerFast
from transformers.models.roberta import RobertaTokenizerFast

from data.data_utils import string_f2h

from .backbone.layoutlmv3 import LayoutLMv3Config, LayoutLMv3Model, LayoutLMv3Processor
from .backbone.lilt import LiltConfig, LiltModel


def fetcher_XLMTokenizer(orig_text: str, tokens: List[str]) -> List[str]:
    """Post-process the tokens from XLMTokenizer to match the original text

    Parameters
    ----------
    orig_text : str
        The original text
    tokens : List[str]
        The tokens generated by the tokenizer

    Returns
    -------
    List[str]
        The original sub-strings that each token corresponds to
    """
    processed_tokens = []
    orig_ptr = 0
    for i, t in enumerate(tokens):
        tt = t.replace("▁", " ")
        new_t = ""
        for s in tt:
            curr_orig_c = orig_text[orig_ptr]
            if s != curr_orig_c and string_f2h(s) != string_f2h(curr_orig_c):
                new_t += ""
            else:
                new_t += curr_orig_c
                orig_ptr += 1
                if (
                    curr_orig_c == " " and orig_text[orig_ptr] == " "
                ):  # skip multiple spaces
                    orig_ptr += 1
                    new_t += " "

        if i == len(tokens) - 1 and orig_ptr < len(orig_text):
            while orig_ptr < len(orig_text):
                new_t += orig_text[orig_ptr]
                orig_ptr += 1

        processed_tokens.append(new_t)

    return processed_tokens


def fetcher_LayoutLMv2Tokenizer(orig_text: str, tokens: List[str]) -> List[str]:
    """Post-process the tokens from LayoutLMv2Tokenizer to match the original text

    Parameters
    ----------
    orig_text : str
        The original text
    tokens : List[str]
        The tokens generated by the tokenizer

    Returns
    -------
    List[str]
        The original sub-strings that each token corresponds to
    """
    if len(orig_text) == 0 or orig_text.isspace():
        return []

    orig_text = orig_text.replace("á", "a")
    orig_text = orig_text.replace("é", "e")
    orig_text = orig_text.replace("í", "i")
    orig_text = orig_text.replace("ó", "o")
    orig_text = orig_text.replace("ú", "u")
    orig_text = orig_text.replace("ü", "u")

    orig_index = 0
    fetched_tokens = []
    for token in tokens:
        real_token = ""
        if token == "[UNK]":
            while orig_text[orig_index] == " ":
                real_token += orig_text[orig_index]
                orig_index += 1
                if orig_index >= len(orig_text):
                    break
            real_token += orig_text[orig_index]
            orig_index += 1
        else:
            if token.startswith("##"):
                token = token[2:]
            for c in token:
                while c != orig_text[orig_index] and c.upper() != orig_text[orig_index]:
                    real_token += orig_text[orig_index]
                    orig_index += 1
                    if orig_index >= len(orig_text):
                        break

                real_token += orig_text[orig_index]
                orig_index += 1

        fetched_tokens.append(real_token)

    appdx = ""
    if orig_index < len(orig_text):
        while orig_index < len(orig_text):
            appdx += orig_text[orig_index]
            orig_index += 1
    fetched_tokens[-1] += appdx

    return fetched_tokens


def fetcher_RobertaTokenizer(orig_text: str, tokens: List[str]) -> List[str]:
    """Post-process the tokens from RobertaTokenizer to match the original text

    Parameters
    ----------
    orig_text : str
        The original text
    tokens : List[str]
        The tokens generated by the tokenizer

    Returns
    -------
    List[str]
        The original sub-strings that each token corresponds to
    """
    if len(orig_text) == 0 or orig_text.isspace():
        return []

    orig_index = 0
    fetched_tokens = []
    for token in tokens:
        real_token = ""
        token = token.replace("Â°", "°")
        token = token.replace("Î¿", "o")
        if token == "<unk>":
            while orig_text[orig_index] == " ":
                real_token += orig_text[orig_index]
                orig_index += 1
                if orig_index >= len(orig_text):
                    break
            real_token += orig_text[orig_index]
            orig_index += 1
        else:
            if token.startswith("Ġ"):
                token = token.replace("Ġ", " ")
            for c in token:
                while c != orig_text[orig_index] and c.upper() != orig_text[orig_index]:
                    real_token += orig_text[orig_index]
                    orig_index += 1
                    if orig_index >= len(orig_text):
                        break

                real_token += orig_text[orig_index]
                orig_index += 1

        fetched_tokens.append(real_token)

    appdx = ""
    if orig_index < len(orig_text):
        while orig_index < len(orig_text):
            appdx += orig_text[orig_index]
            orig_index += 1
    fetched_tokens[-1] += appdx

    return fetched_tokens


def fetcher_LayoutLMv3Tokenizer(orig_text: str, tokens: List[str]) -> List[str]:
    """Post-process the tokens from LayoutLMv3Tokenizer to match the original text

    Parameters
    ----------
    orig_text : str
        The original text
    tokens : List[str]
        The tokens generated by the tokenizer

    Returns
    -------
    List[str]
        The original sub-strings that each token corresponds to
    """
    if len(orig_text) == 0 or orig_text.isspace():
        return []

    orig_index = 0
    fetched_tokens = []
    for i, token in enumerate(tokens):
        real_token = ""
        token = token.replace("Â°", "°")
        token = token.replace("Î¿", "o")
        if token == "<unk>":
            while orig_text[orig_index] == " ":
                real_token += orig_text[orig_index]
                orig_index += 1
                if orig_index >= len(orig_text):
                    break
            real_token += orig_text[orig_index]
            orig_index += 1
        else:
            if token.startswith("Ġ"):
                token = token.replace("Ġ", " ") if i > 0 else token.replace("Ġ", "")
            for c in token:
                while c != orig_text[orig_index] and c.upper() != orig_text[orig_index]:
                    real_token += orig_text[orig_index]
                    orig_index += 1
                    if orig_index >= len(orig_text):
                        break

                real_token += orig_text[orig_index]
                orig_index += 1

        fetched_tokens.append(real_token)

    appdx = ""
    if orig_index < len(orig_text):
        while orig_index < len(orig_text):
            appdx += orig_text[orig_index]
            orig_index += 1
    fetched_tokens[-1] += appdx

    return fetched_tokens


class LayoutLMv3ChineseProcessor(LayoutLMv3Processor):
    tokenizer_class = ("XLMRobertaTokenizer", "XLMRobertaTokenizerFast")


@dataclass
class BackboneInfo:
    model: PreTrainedModel
    config: PretrainedConfig
    hf_name: str
    processor: Optional[Union[ProcessorMixin, PreTrainedTokenizerBase]] = None
    image_processor: Optional[ImageProcessingMixin] = None
    max_token_len: Optional[int] = 512
    add_cls_token: Optional[bool] = False
    add_sep_token: Optional[bool] = False
    has_visual_embeds: Optional[bool] = False
    tokenizer_fetcher: Optional[Callable] = None


# ! DO NOT change the order of this dictionary,
# ! as the weight generation script depends on it
BACKBONE_MAPPING = {
    "lilt-infoxlm-base": BackboneInfo(
        model=LiltModel,
        config=LiltConfig,
        hf_name="SCUT-DLVCLab/lilt-infoxlm-base",
        processor=LayoutXLMTokenizerFast,
        image_processor=None,
        max_token_len=511,
        add_cls_token=True,
        add_sep_token=False,
        has_visual_embeds=False,
        tokenizer_fetcher=fetcher_XLMTokenizer,
    ),
    "lilt-roberta-en-base": BackboneInfo(
        model=LiltModel,
        config=LiltConfig,
        hf_name="SCUT-DLVCLab/lilt-roberta-en-base",
        processor=RobertaTokenizerFast,
        image_processor=None,
        max_token_len=511,
        add_cls_token=True,
        add_sep_token=False,
        has_visual_embeds=False,
        tokenizer_fetcher=fetcher_RobertaTokenizer,
    ),
    "layoutxlm-base": BackboneInfo(
        model=LayoutLMv2Model,
        config=LayoutLMv2Config,
        hf_name="microsoft/layoutxlm-base",
        processor=LayoutXLMProcessor,
        image_processor=LayoutLMv2ImageProcessor,
        max_token_len=511,
        add_cls_token=True,
        add_sep_token=False,
        has_visual_embeds=True,
        tokenizer_fetcher=fetcher_XLMTokenizer,
    ),
    "layoutlmv2-base-uncased": BackboneInfo(
        model=LayoutLMv2Model,
        config=LayoutLMv2Config,
        hf_name="microsoft/layoutlmv2-base-uncased",
        processor=LayoutLMv2Processor,
        image_processor=LayoutLMv2ImageProcessor,
        max_token_len=511,
        add_cls_token=True,
        add_sep_token=False,
        has_visual_embeds=True,
        tokenizer_fetcher=fetcher_LayoutLMv2Tokenizer,
    ),
    "layoutlmv3-base-chinese": BackboneInfo(
        model=LayoutLMv3Model,
        config=LayoutLMv3Config,
        hf_name="microsoft/layoutlmv3-base-chinese",
        processor=LayoutLMv3ChineseProcessor,
        image_processor=LayoutLMv3ImageProcessor,
        max_token_len=510,
        add_cls_token=True,
        add_sep_token=True,
        has_visual_embeds=True,
        tokenizer_fetcher=fetcher_XLMTokenizer,
    ),
    "layoutlmv3-base": BackboneInfo(
        model=LayoutLMv3Model,
        config=LayoutLMv3Config,
        hf_name="microsoft/layoutlmv3-base",
        processor=LayoutLMv3Processor,
        image_processor=LayoutLMv3ImageProcessor,
        max_token_len=510,
        add_cls_token=True,
        add_sep_token=True,
        has_visual_embeds=True,
        tokenizer_fetcher=fetcher_LayoutLMv3Tokenizer,
    ),
}