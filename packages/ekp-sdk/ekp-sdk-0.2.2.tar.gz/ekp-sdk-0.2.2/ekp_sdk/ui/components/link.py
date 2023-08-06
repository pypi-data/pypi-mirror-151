from ekp_sdk.util.clean_null_terms import clean_null_terms


def Link(
        class_name=None,
        content=None,
        external=None,
        externalIcon=None,
        href=None,
        style=None,
        tooltip=None
):
    return {
        "_type": "Link",
        "props": clean_null_terms({
            "class_name": class_name,
            "content": content,
            "external": external,
            "externalIcon": externalIcon,
            "href": href,
            "style": style,
            "tooltip": tooltip,
        })
    }
