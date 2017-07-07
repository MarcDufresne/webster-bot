import slugify

to_lower = slugify.Slugify(to_lower=True)
make_key = slugify.Slugify(to_lower=True, safe_chars='_')
