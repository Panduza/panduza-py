

export PZA_ALIASES='{
    "local": {
        "url": "localhost",
        "port": 1883,
        "interfaces": {
            "fake_psu_0": "pza/default/Panduza_FakePsu/channel_0",
            "fake_psu_1": "pza/default/Panduza_FakePsu/channel_1"
        }
    }
}'


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo PZA_ALIASES=$PZA_ALIASES > $SCRIPT_DIR/fake_bench.env
