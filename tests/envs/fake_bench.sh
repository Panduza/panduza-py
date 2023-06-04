

export PZA_ALIASES='{
    "local": {
        "url": "localhost",
        "port": 1883,
        "interfaces": {
            "psu_1": "pza/default/Panduza_FakePsu/channel_0"
        }
    }
}'


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo PZA_ALIASES=$PZA_ALIASES > $SCRIPT_DIR/fake_bench.env
