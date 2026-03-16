import asyncio, aiohttp, csv, ipaddress, textwrap
from urllib.parse import urlparse
from collections import defaultdict
from pyvis.network import Network
from tabulate import tabulate

URLHAUS="https://urlhaus.abuse.ch/downloads/csv_recent/"
ASN_FILE="ip2asn-v4.tsv"

MAX_IPS=400

ranges=[]


# load ASN ranges
def load_asn():
    with open(ASN_FILE,encoding="utf-8") as f:
        for line in f:
            p=line.strip().split("\t")
            if len(p)<5:
                continue
            try:
                start=int(ipaddress.IPv4Address(p[0]))
                end=int(ipaddress.IPv4Address(p[1]))
                asn=int(p[2])
                name=p[4]
                ranges.append((start,end,asn,name))
            except:
                pass


# ASN lookup
def lookup_asn(ip):
    i=int(ipaddress.IPv4Address(ip))
    for s,e,a,n in ranges:
        if s<=i<=e:
            return a,n
    return None,None


def is_ip(h):
    try:
        ipaddress.ip_address(h)
        return True
    except:
        return False


# fetch IP URLs from URLHaus
async def fetch_ips():

    async with aiohttp.ClientSession() as s:
        async with s.get(URLHAUS) as r:
            text=await r.text()

    reader=csv.reader(text.splitlines())

    ip_urls=defaultdict(list)

    for row in reader:

        if not row or row[0].startswith("#"):
            continue

        try:

            url=row[2]
            host=urlparse(url).netloc.split(":")[0]

            if is_ip(host):
                ip_urls[host].append(url)

        except:
            pass

    ips=list(ip_urls.keys())[:MAX_IPS]

    return ips,ip_urls


# process IP enrichment
async def process(ips,ip_urls):

    results=[]

    for ip in ips:

        asn,name=lookup_asn(ip)

        urls=ip_urls[ip]

        results.append((ip,asn,name,urls))

    return results


# terminal output
def terminal_output(data):

    rows=[[ip,f"AS{a}" if a else "",n or "",len(urls)] for ip,a,n,urls in data]

    print("\nIP Infrastructure\n")

    print(tabulate(
        rows,
        headers=["IP","ASN","Network","URL Count"],
        tablefmt="simple"
    ))


    asn_ips=defaultdict(list)
    asn_names={}

    for ip,a,n,urls in data:

        if a:
            asn_ips[a].append(ip)
            asn_names[a]=n


    asn_rows=[]

    for asn,ips in sorted(asn_ips.items(),key=lambda x:len(x[1]),reverse=True):

        ips=sorted(ips)

        asn_rows.append([
            f"AS{asn}",
            asn_names[asn],
            len(ips),
            textwrap.fill(", ".join(ips),80)
        ])

    print("\nASN Infrastructure Clusters\n")

    print(tabulate(
        asn_rows,
        headers=["ASN","Network","IPs","IP List"],
        tablefmt="simple"
    ))


# graph
def export_graph(data):

    ip_set=set()
    asn_ips=defaultdict(list)
    asn_map={}
    asn_names={}
    ip_urls={}

    for ip,a,n,urls in data:

        ip_set.add(ip)
        ip_urls[ip]=urls

        if a:
            asn_ips[a].append(ip)
            asn_map[ip]=(a,n)
            asn_names[a]=n


    net=Network(
        height="100%",
        width="100%",
        bgcolor="#0f172a",
        font_color="#e2e8f0"
    )

    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "forceAtlas2Based": {
          "gravitationalConstant": -150,
          "centralGravity": 0.01,
          "springLength": 180,
          "springConstant": 0.02,
          "avoidOverlap": 1
        },
        "solver": "forceAtlas2Based",
        "stabilization": { "iterations": 300 }
      }
    }
    """)

    # ASN nodes
    for asn,ips in sorted(asn_ips.items(),key=lambda x:len(x[1]),reverse=True):

        tooltip="<br>".join(sorted(ips))

        name=asn_names.get(asn,"")

        net.add_node(
            f"asn:{asn}",
            label=f"AS{asn}\n{name}\n{len(ips)} IPs",
            title=tooltip,
            color="#22c55e",
            size=50
        )


    # IP nodes
    for ip,a,n,urls in data:

        tooltip="<br>".join(urls)

        net.add_node(
            f"ip:{ip}",
            label=f"{ip}\n{len(urls)} URLs",
            title=tooltip,
            color="#38bdf8",
            size=30
        )

        if a:
            net.add_edge(
                f"ip:{ip}",
                f"asn:{a}",
                width=3,
                color="#94a3b8"
            )


    net.write_html("graph.html")


    sidebar=f"""
<div class="sidebar">

<h1>Threat Infrastructure</h1>

<div class="metrics">

<div class="card">
<h3>IPs</h3>
<p>{len(ip_set)}</p>
</div>

<div class="card">
<h3>ASNs</h3>
<p>{len(asn_ips)}</p>
</div>

</div>

<h2>ASN Clusters</h2>
"""

    for asn,ips in sorted(asn_ips.items(),key=lambda x:len(x[1]),reverse=True):

        ips=sorted(ips)

        name=asn_names.get(asn,"Unknown Network")

        sidebar+=f"""
<details class="tbl">
<summary>AS{asn} — {name} — {len(ips)} IPs</summary>
<div style="padding-top:6px;font-size:13px;">
{"<br>".join(ips)}
</div>
</details>
"""


    sidebar+="</div>"


    css="""
<style>

body{
margin:0;
display:flex;
font-family:system-ui;
background:#0f172a;
color:#e2e8f0;
}

.sidebar{
width:380px;
padding:28px;
background:#020617;
border-right:1px solid #1e293b;
overflow:auto;
}

.sidebar h1{
margin-top:0;
font-size:22px;
}

.sidebar h2{
margin-top:30px;
font-size:16px;
border-bottom:1px solid #1e293b;
padding-bottom:6px;
}

.metrics{
display:grid;
grid-template-columns:1fr 1fr;
gap:10px;
margin-top:20px;
}

.card{
background:#020617;
border:1px solid #1e293b;
padding:14px;
border-radius:6px;
}

.card h3{
margin:0;
font-size:12px;
color:#94a3b8;
}

.card p{
margin:4px 0 0 0;
font-size:20px;
font-weight:600;
}

.tbl{
margin-top:10px;
border:1px solid #1e293b;
border-radius:6px;
padding:8px;
background:#020617;
}

summary{
cursor:pointer;
font-size:13px;
color:#e2e8f0;
}

#mynetwork{
flex:1;
height:100vh;
}

</style>
"""


    with open("graph.html","r",encoding="utf-8") as f:
        html=f.read()

    html=html.replace("<body>",f"<body>{sidebar}")
    html=html.replace("</head>",f"{css}</head>")

    with open("graph.html","w",encoding="utf-8") as f:
        f.write(html)

    print("\nGraph exported: graph.html")


# main
async def main():

    load_asn()

    ips,ip_urls=await fetch_ips()

    data=await process(ips,ip_urls)

    terminal_output(data)

    export_graph(data)


asyncio.run(main())