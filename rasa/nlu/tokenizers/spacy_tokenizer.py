import typing
from typing import Text, List, Any

from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.nlu.utils.spacy_utils import SpacyNLP
from rasa.nlu.training_data import Message

from rasa.nlu.constants import TOKENS_NAMES, SPACY_DOCS, DENSE_FEATURIZABLE_ATTRIBUTES

if typing.TYPE_CHECKING:
    from spacy.tokens.doc import Doc  # pytype: disable=import-error

try:
    import spacy
except ImportError:
    spacy = None


class SpacyTokenizer(Tokenizer):

    provides = [TOKENS_NAMES[attribute] for attribute in DENSE_FEATURIZABLE_ATTRIBUTES]

    requires = [SPACY_DOCS[attribute] for attribute in DENSE_FEATURIZABLE_ATTRIBUTES]

    required_components = [SpacyNLP.name]

    defaults = {
        # Flag to check whether to split intents
        "intent_tokenization_flag": False,
        # Symbol on which intent should be split
        "intent_split_symbol": "_",
    }

    def get_doc(self, message: Message, attribute: Text) -> "Doc":
        return message.get(SPACY_DOCS[attribute])

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        doc = self.get_doc(message, attribute)

        return [
            Token(t.text, t.idx, lemma=t.lemma_, data={"pos": self._tag_of_token(t)})
            for t in doc
        ]

    @staticmethod
    def _tag_of_token(token: Any) -> Text:
        if spacy.about.__version__ > "2" and token._.has("tag"):
            return token._.get("tag")
        else:
            return token.tag_
