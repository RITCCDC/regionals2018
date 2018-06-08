# Import A records from CSV file.

param (
     [Parameter(Mandatory=$true)][string]$Filename
)

$csv = Import-Csv $Filename
foreach ($record in $csv){
     Add-DnsServerResourceRecordA -Name $record.Name -IPv4Address $record.Address -ZoneName team4.wildeagle.local
}
