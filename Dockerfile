FROM ghcr.io/mdw-nl/datavalgen:v0.3.0

# default model and factory
ENV DATAVALGEN_DISTRIBUTION=datavalgen-model-example
ENV DATAVALGEN_MODEL=example
ENV DATAVALGEN_FACTORY=example

COPY ./src /app/datavalgen-model-example/src
COPY ./pyproject.toml /app/datavalgen-model-example/pyproject.toml
COPY ./README.md /app/datavalgen-model-example/README.md

# install example data model package, where already-installed datavalgen can
# find models and factories via python entry-points
RUN pip install --no-cache-dir /app/datavalgen-model-example
