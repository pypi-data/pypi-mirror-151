# Abstractive
This project is a convenient part of the NLP project, including several already exposed projects such as summy and text processing. One of the main functions is sentence token in japanese.

The open resources we use are:
- rouge [Apache-2.0 license]: https://github.com/pltrdy/rouge
- summy [Apache-2.0 license]: https://github.com/miso-belica/sumy
- nltk [Apache-2.0 license]: https://pypi.org/project/nltk/
- jieba [MIT License (MIT)]: https://pypi.org/project/jieba/
- MeCab [BSD License (BSD)]: https://pypi.org/project/mecab-python3/
- SudachiPy [Apache-2.0 license]: https://pypi.org/project/SudachiPy/

# Examples

The sentence token example.

```python
>>> from util_ds.nlp.sentence_token import sentenceToken
>>> sentence = "ドイツ連邦共和国（ドイツれんぽうきょうわこく、独: Bundesrepublik Deutschland）、通称ドイツ（独: Deutschland）は、中央ヨーロッパ西部に位置する連邦共和制国家。首都および最大の都市（英語版）はベルリン[1]。南がスイスとオーストリア、北にデンマーク、西をフランスとオランダとベルギーとルクセンブルク、東はポーランドとチェコとそれぞれ国境を接する。"
>>> sentences = sentenceToken("japanese", sentence)
>>> ["ドイツ連邦共和国（ドイツれんぽうきょうわこく、独: Bundesrepublik Deutschland）、通称ドイツ（独: Deutschland）は、中央ヨーロッパ西部に位置する連邦共和制国家。首都および最大の都市（英語版）はベルリン[1]。", "南がスイスとオーストリア、北にデンマーク、西をフランスとオランダとベルギーとルクセンブルク、東はポーランドとチェコとそれぞれ国境を接する。"]
```

Notes: The above functions can basically be replaced by the following functions.

```python
>>> import re
>>> # Didn't consider the more complicated case here.
>>> def sentenceToken(language, text):
>>>     pattern = '([。！？\?])([^」』）])'
>>>     sentences = re.sub(pattern, r"\1\n\2", text).split("\n")
>>>     sentences = list(map(lambda x: x.strip(), sentences))
>>>     sentences = list(filter(lambda x: x!="", sentences))
>>>     return sentences
```