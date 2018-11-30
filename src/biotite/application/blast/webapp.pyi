# This source code is part of the Biotite package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

from typing import Optional, List, Union
from subprocess import Popen
from ..webapp import WebApp
from .alignment import BlastAlignment
from ..sequence.seqtypes import ProteinSequence, NucleotideSequence
from ...database.entrez import Query


class BlastWebApp(WebApp):
    def __init__(
        self,
        program: str,
        query: Union[ProteinSequence, NucleotideSequence, str],
        database: str = "nr",
        app_url: str = "https://blast.ncbi.nlm.nih.gov/Blast.cgi",
        obey_rules: bool = True,
        mail: Optional[str] = None
    ) -> None: ...
    def set_entrez_query(self, query: Query) -> None: ...
    def set_max_results(self, number: int) -> None: ...
    def set_max_expect_value(self, value: float) -> None: ...
    def set_gap_penalty(self, opening: float, extension: float) -> None: ...
    def set_word_size(self, size: int) -> None: ...
    def set_match_reward(self, reward: int) -> None: ...
    def set_mismatch_penalty(self, penalty: int) -> None: ...
    def set_substitution_matrix(self, matrix_name: str) -> None: ...
    def set_threshold(self, threshold: int) -> None: ...
    def run(self) -> None: ...
    def is_finished(self) -> bool: ...
    def wait_interval(self) -> int: ...
    def clean_up(self) -> None: ...
    def evaluate(self) -> None: ...
    def get_xml_response(self) -> str: ...
    def get_alignments(self) -> List[BlastAlignment]: ...