class BaseAnnotator:

    @staticmethod
    def annotate(**kwargs):
        pass


class CSTitleAnnotator(BaseAnnotator):

    @staticmethod
    def annotate(text):
        pass


class CSAbstractAnnotator(BaseAnnotator):

    @staticmethod
    def annotate(text):
        pass


class CSAnnotator(BaseAnnotator):

    @staticmethod
    def annotate(title, abstract):
        return {
            'title_entities': CSAbstractAnnotator.annotate(text=title),
            'abstract_entities': CSAnnotator.annotate(text=abstract)
        }
