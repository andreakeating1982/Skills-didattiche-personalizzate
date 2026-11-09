import sys, unittest
from pathlib import Path
from tempfile import TemporaryDirectory
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from verifica_quiz_fonti_obbligatori import verify

class GateQuizFontiTests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory(); self.file=Path(self.tmp.name)/'doc.html'
    def tearDown(self): self.tmp.cleanup()
    def build(self,n=10,ref=True,options=4,notes=True,index=True,instruction=None,expected=None):
        nav='<nav><a href="#verifica">Verifica</a><a href="#mapa">Mappa</a><a href="#referencias">Fonti</a></nav>' if index else ''
        cards=''.join('<div class="quiz-card"><table><tr>'+''.join('<td>'+c+'. opzione '+str(i)+'</td>' for c in 'ABCD'[:options])+'</tr></table></div>' for i in range(n))
        nr='<sup><a href="#rif-1">[1]</a></sup>' if notes else ''
        bibliografia='<section id="referencias"><div class="ref-entry" id="rif-1" data-bibliography-entry>Fonte reale</div></section>' if ref else ''
        intro='<p class="quiz-intro">'+instruction+'</p>' if instruction is not None else ''
        self.file.write_text('<html><body>'+nav+'<p>Testo '+nr+'</p><section id="verifica">'+intro+cards+'</section><section id="mapa"></section>'+bibliografia+'</body></html>')
        return verify(self.file,expected_instruction=expected)
    def test_10_domande_e_fonti_supera(self):self.assertTrue(self.build()['passed'])
    def test_domande_mancanti_bloccano(self):self.assertFalse(self.build(n=9)['passed'])
    def test_fonti_mancanti_bloccano(self):self.assertFalse(self.build(ref=False)['passed'])
    def test_opzioni_incomplete_bloccano(self):self.assertFalse(self.build(options=3)['passed'])
    def test_note_mancanti_bloccano(self):self.assertFalse(self.build(notes=False)['passed'])
    def test_indice_mancante_blocca(self):self.assertFalse(self.build(index=False)['passed'])
    def test_consegna_esatta_supera(self):
        s='Elige una sola respuesta para cada pregunta.'
        self.assertTrue(self.build(instruction=s,expected=s)['passed'])
    def test_consegna_diversa_blocca(self):
        s='Elige una sola respuesta para cada pregunta.'
        self.assertFalse(self.build(instruction='Lee y responde.',expected=s)['passed'])
    def test_consegna_mancante_blocca(self):
        self.assertFalse(self.build(expected='Elige una sola respuesta para cada pregunta.')['passed'])
if __name__=='__main__':unittest.main()

