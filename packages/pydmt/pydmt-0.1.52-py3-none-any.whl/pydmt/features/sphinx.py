import os

from pydmt.api.feature import Feature
from pydmt.builders.sphinx import BuilderSphinx
from pydmt.core.pydmt import PyDMT

SPHINX_FOLDER = "sphinx"


class FeatureSphinx(Feature):
    def setup(self, pydmt: PyDMT) -> None:
        # pylint: disable=import-outside-toplevel
        try:
            import config.project
            name = config.project.name
        except ModuleNotFoundError:
            return
        if not os.path.isdir(SPHINX_FOLDER):
            return
        pydmt.add_builder(BuilderSphinx(package_name=name))
