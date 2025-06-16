from medkit.core.text import TextDocument
from medkit.text.ner.hf_entity_matcher import HFEntityMatcher
from medkit.core.pipeline import Pipeline, PipelineStep
from medkit.text.spacy.edsnlp import EDSNLPPipeline
import spacy
from pathlib import Path

from medkit.text.segmentation import SentenceTokenizer
# Segmentation
sent_tokenizer = SentenceTokenizer(output_label="sentence")
# Entity recognition
entity_matcher = HFEntityMatcher(model="camila-ud/DrBERT-CASM2")

nlp = spacy.blank("eds")
nlp.add_pipe("eds.dates")
eds_nlp_pipeline = EDSNLPPipeline(nlp)

# 2. Combine operations into a pipeline.
from medkit.core.pipeline import Pipeline, PipelineStep

ner_pipeline = Pipeline(
    input_keys=["full_text"],
    output_keys=["entities"],
    steps=[
        PipelineStep(sent_tokenizer, input_keys=["full_text"], output_keys=["sentences"]),
        PipelineStep(entity_matcher, input_keys=["sentences"], output_keys=["entities"]),
        PipelineStep(operation=eds_nlp_pipeline, input_keys=["sentences"], output_keys=["entities"])
    ],
)

docs = TextDocument.from_dir(Path("C:/Users/mathu/Documents/2024-2025/Stage/Texte"))
entities = ner_pipeline.run([d.raw_segment for d in docs])
print(entities)