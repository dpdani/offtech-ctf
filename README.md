# offtech-ctf

### Analyzer

From your local machine launch:

```
ssh -T <username>@users.isi.deterlab.net ssh -T <host>.ctf-resilient-g3.offtech "sudo tcpdump -s0 -U --immediate-mode -nn -i <interface> -w -" | python3 analyze_pcap.py
```

NB: requires `pyshark` and `flask` installed on your local machine


### Attacks

To launch an attack, first discover its name by looking at the `Attack` enum in
`red/attacks/__init__.py`, then run:

```bash
./redder attack my-attack --bps 100MB
```

or

```bash
./redder attack my-attack --pps 100
```

Depending on the attack one or more option may be available, but note that they 
cannot be used together.
