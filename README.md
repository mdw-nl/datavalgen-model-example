 # datavalgen-model-example

This is an example of a pydantic model for a fictional dataset.

It's packaged in python package ready to be used by datavalgen – trivial little
tool that just provides an "easier" way of validating data against a
pydantic model like the one include here.

The example schema is grouped into a few clearly separate parts:

- Identity/Admin:
  `id`, `name`, `site_code`, `record_source`
- Demographics:
  `age`, `sex`, `height_cm`, `weight_kg`
- Episode/Dates:
  `start_date`, `end_date`, `admission_date`, `discharge_date`
- Clinical/Outcome:
  `status`, `smoker`, `diagnosis_code`, `symptom_score`,
  `response_status`, `mortality_30d`

The package registers multiple selectable models under
`[project.entry-points."datavalgen.models"]`:

- `example` and `example_full`: the full fictional dataset
- `example_identity_admin`
- `example_demographics`
- `example_episode_dates`
- `example_clinical_outcome`
- `example_demographics_clinical_outcome`

`datavalgen validate` requires the selected model's columns to be present.
Extra CSV columns are ignored with a warning, so a subset model can be
validated against a wider dataset.

## Validation Example

Scenario: You have some data in a csv that needs to be validated against one of
the schemas included in this image. Example files are included in the `data`
directory.

So, it looks like this:
```
$ tree data
data
├── clinical_outcome.csv
├── demographics.csv
├── demographics_clinical_outcome.csv
└── tiny.csv

1 directory, 4 files
```

You can validate the full schema with something like:
```
$ docker run \
  --network none --rm --read-only --cap-drop=ALL --security-opt no-new-privileges=true --log-driver=none --user $(id -u):$(id -g) \
  -v ./data/tiny.csv:/data.csv:ro \
  ghcr.io/mdw-nl/datavalgen-model-example:v0.3.0rc1 \
  validate
✅ No validation errors found.
```

Or validate one of the smaller registered models:
```
$ docker run \
  --network none --rm --read-only --cap-drop=ALL --security-opt no-new-privileges=true --log-driver=none --user $(id -u):$(id -g) \
  -v ./data/clinical_outcome.csv:/data.csv:ro \
  ghcr.io/mdw-nl/datavalgen-model-example:v0.3.0rc1 \
  validate -m example_clinical_outcome
✅ No validation errors found.
```

> [!IMPORTANT]
> The options `--network none --rm --log-driver=none --read-only --cap-drop=ALL
> --security-opt no-new-privileges=true --user $(id -u):$(id -g)` run this image
> in a more locked-down way: they disable networking, prevent writes to the image
> filesystem, drop most extra operating system (OS) privileges, and tell Docker
> not to store container logs (you still see output in your terminal). This image
> is not expected to need any of those capabilities, so these flags are simply
> defense in depth, especially when you use real, private datasets. Please use them!


If there are errors, you will see output like this:
```
$ docker run \
  --network none --rm --read-only --cap-drop=ALL --security-opt no-new-privileges=true --log-driver=none --user $(id -u):$(id -g) \
  -v ./data/tiny.csv:/data.csv:ro \
  ghcr.io/mdw-nl/datavalgen-model-example:v0.3.0rc1 \
  validate
❌ Line 2, column 'age': Input should be less than or equal to 120.
   Got: '550'.
⚠️  Note: errors above contain your actual data values ("Got: .."). Do not share.
```

> [!NOTE]
> Note that "❌ Line 2" referes to the second line on the file itself, as you
> might see it in a simple editor. Line 1 would be the header, and line 2 would be
> the first row of data.
