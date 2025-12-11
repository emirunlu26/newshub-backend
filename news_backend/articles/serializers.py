def serialize_tag(tag):
    return {
        "id": tag.id,
        "name": tag.name,
        "slug": tag.slug
    }