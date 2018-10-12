# Import A records from CSV file.

param (
     [Parameter(Mandatory=$true)][string]$Filename,
     [Parameter(Mandatory=$true)][string]$TeamNumber
)

$csv = Import-Csv $Filename
foreach ($record in $csv){
    $ZoneName = "team" + $TeamNumber + ".wildeagle.local"
     Add-DnsServerResourceRecordA -Name $record.Name -IPv4Address $record.Address -ZoneName $ZoneName
}
