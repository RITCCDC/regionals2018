$Users = Import-Csv -Path "C:\users.csv"

$Domain = (Get-ADDomain | select -expand dnsroot)

foreach ($User in $Users)
{
     $DisplayName = $User.username
     $SAM = $User.sam
     $Description = $User.role
     $Password = $User.password
     $Email = $SAM + "@" + $domainname
     New-ADUser -Name "$DisplayName" -DisplayName "$DisplayName" -SamAccountName $SAM -Description "$Descrption" -AccountPassword (ConvertTo-SecureString $Password -AsPlainText -Force) -EmailAddress $Email -Enabled $true -ChangePasswordAtLogon $false -PasswordNeverExpires $true
}
