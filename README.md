# offtech-ctf

### Analyzer

First run the `capture.sh` script in the control server.

Then from your local machine launch:

```
ssh -T otech2ai@users.isi.deterlab.net ssh -T server.ctf-resilient-g3.offtech "tail -f -n +1 ~/CCTF-Resilient-Server/blue/pcap.pcap" | python3 analyze_pcap.py
```

NB: requires pyshark installed in your local machine
