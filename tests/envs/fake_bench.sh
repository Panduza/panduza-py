

export PZA_ALIASES='{
    "local": {
        "url": "localhost",
        "port": 1883,
        "interfaces": {
            "fake_relay_0": "pza/default/Panduza_FakeRelayController/channel_0",
            "fake_ammeter_0": "pza/default/Panduza_FakePsu/channel_0_am",
            "fake_ammeter_1": "pza/default/Panduza_FakePsu/channel_1_am",
            "fake_voltmeter_0": "pza/default/Panduza_FakePsu/channel_0_vl",
            "fake_voltmeter_1": "pza/default/Panduza_FakePsu/channel_1_vl",
            "fake_psu_0": "pza/default/Panduza_FakePsu/channel_0",
            "fake_psu_1": "pza/default/Panduza_FakePsu/channel_1",
            "fake_dio_0": "pza/default/Panduza_FakeDioController/dio_0",
            "fake_dio_1": "pza/default/Panduza_FakeDioController/dio_1"
        }
    }
}'


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo PZA_ALIASES=$PZA_ALIASES > $SCRIPT_DIR/fake_bench.env
