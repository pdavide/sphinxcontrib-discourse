# Sphinx extension that embeds a Discourse topic inside a page

## Installation

```console
pip install git+https://github.com/pdavide/sphinxcontrib-discourse
```

Add `sphinxcontrib.discourse` to `extensions` in your `conf.py`.
Add your documentation domain to "Enabled Domains" in your Discourse admin
settings.

## Usage

In your `conf.py` add a `discourse_url` variable containing the URL if your
Discourse instance (with http:// or https:// and trailing slash).

Insert the `discourse` directive in the rST source of your documentation like
this:
```rst
.. discourse::
   :topic_identifier: <topic_id>
```
where `<topic_id>` is a number identifying a topic in a Discourse instance.
To find a `topic_id` refer to this general Discourse URL structure:
`/t/<topic_name>{/<topic_id>{/<post_id>}}}`.

## References

- [Embedding Discourse Comments via Javascript](https://meta.discourse.org/t/embedding-discourse-comments-via-javascript/31963)

## Licenses

`BSD-3-Clause`.
