# Django:
from django import forms
from django.urls import reverse

# Thirdparty:
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# Localfolder:
from .parsers.alfa_bank_account_report import AlfaBankAccountCSVParser
from .parsers.alfa_card_parser import AlfaBankCardCSVParser
from .parsers.mtbank_parser import MTbankPDFParser
from .parsers.priorbank_csv import PriorbankCSVParser
from .parsers.priorbank_parser import PriorbankPDFParser
from .parsers.sbssberbank_parser import SberbankPDFParser

ALFABANK_ACCOUNT = "1"
ALFABANK_CARD = "2"
MTBANK_PDF = "3"
PRIORBANK_CSV = "4"
PRIORBANK_PDF = "5"
SBERBANK_PDF = "6"


PARSER_MAPPING = {
    ALFABANK_ACCOUNT: AlfaBankAccountCSVParser,
    ALFABANK_CARD: AlfaBankCardCSVParser,
    PRIORBANK_PDF: PriorbankPDFParser,
    SBERBANK_PDF: SberbankPDFParser,
    MTBANK_PDF: MTbankPDFParser,
    PRIORBANK_CSV: PriorbankCSVParser,
}


PARSER_CHOICES = (
    (ALFABANK_ACCOUNT, "AlfaBank Account"),
    (ALFABANK_CARD, "AlfaBank Card"),
    (PRIORBANK_PDF, "Priorbank PDF"),
    (SBERBANK_PDF, "Sberbank PDF"),
    (MTBANK_PDF, "MTBank PDF"),
    (PRIORBANK_CSV, "Priorbank CSV"),
)


class UploadTransactionFileForm(forms.Form):
    parser = forms.ChoiceField(
        choices=PARSER_CHOICES,
        label="",
        initial="",
        widget=forms.Select(),
        required=True,
    )
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "upload-transaction-file"
        self.helper.form_class = "UploadTransactionFile"
        self.helper.form_method = "post"
        self.helper.form_action = reverse("base:upload-transaction-file")
        self.helper.add_input(Submit("submit", "Upload"))
