 # datavalgen-model-example

This is an example of a pydantic model for a simple dataset.

It's packaged in python package ready to be used by datavalgen – trivial little
tool that just provides an "easier" way of validating data against a
pydantic model like the one include here.

## Validation Example

Scenario: You have some data in a csv that needs to be validated against the
schema included in this image. You have the data in a directory called `data`
and the file is called `tiny.csv`.

So, it looks like this:
```
$ tree data
data
└── tiny.csv

1 directory, 1 file
```

You can validate with something like:
```
$ docker run \
  --network none --rm --read-only --cap-drop=ALL --security-opt no-new-privileges=true --log-driver=none --user $(id -u):$(id -g) \
  -v ./data/tiny.csv:/data.csv:ro \
  ghcr.io/mdw-nl/datavalgen-model-example:v0.1.0 \
  validate
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
  ghcr.io/mdw-nl/datavalgen-model-example:v0.1.0 \
  validate
❌ Line 2, column 'age': Input should be less than or equal to 120.
   Got: '550'.
⚠️  Note: errors above contain your actual data values ("Got: .."). Do not share.
```

> [!NOTE]
> Note that "❌ Line 2" referes to the second line on the file itself, as you
> might see it in a simple editor. Line 1 would be the header, and line 2 would be
> the first row of data.
