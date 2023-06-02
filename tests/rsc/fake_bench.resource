*** Settings ***

Library      panduza.robof.Keywords
# Variables    envs/fake_bench.py


*** Variables ***
${pza_aliases}      %{PZA_ALIASES}



*** Keywords ***

Setup Bench Config
    Set Log Level    DEBUG
    Log     ${pza_aliases}
    Load Pza Interfaces From Aliases    ${pza_aliases}
