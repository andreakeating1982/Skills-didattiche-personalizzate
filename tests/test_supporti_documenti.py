from pathlib import Path
import importlib.util
ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location("supporti_skill",ROOT/"skills/quaderno-accessibile/tests/test_integrazioni.py")
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
SpecchiettiTests=m.SpecchiettiTests
