# Mitre_analysis
This code return a list of Mitre tactics, tachniques and sub-tachniques in IDs which can be used by secrity platform to measure the coverage of these available techniques against the techniques they are using in their current platform.

Data retruned by this script will be in format:

{Tactic:[{techniques:sub-tachniques},{techniques:sub-tachniques} ... ]}

like:

{'TA0043': [{'T1595': ['T1595.001', 'T1595.002', 'T1595.003']}, {'T1592': ['T1592.001', 'T1592.002', 'T1592.003', 'T1592.004']}, {'T1589': ['T1589.001', 'T1589.002', 'T1589.003']},