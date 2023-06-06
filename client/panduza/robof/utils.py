from hamcrest import assert_that, equal_to, any_of, has_key

bstr_map = {
    "on": True,
    "off": False,
    "true": True,
    "false": False,
    "True": True,
    "False": False,
}

def boolean_str_to_boolean(bstr):
    assert_that( bstr_map, has_key(bstr) )
    return bstr_map[bstr]
