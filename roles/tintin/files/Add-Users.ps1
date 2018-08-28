$Users = Import-Csv -Path "C:\users.csv"

foreach ($User in $Users)
{
    if (-not (@(Get-ADUser -Filter { SamAccountName -eq $User.sam }).Count -eq 0)) {
        Remove-ADUser -Identity $User.sam
    }
     $DisplayName = $User.username
     $SAM = $User.sam
     $Description = $User.role
     $Password = $User.password
     $Email = $SAM + "@team4.wildeagle.local"
     New-ADUser -Name "$DisplayName" -DisplayName "$DisplayName" -SamAccountName $SAM -Description "$Description" -AccountPassword (ConvertTo-SecureString $Password -AsPlainText -Force) -EmailAddress $Email -Enabled $true -ChangePasswordAtLogon $false -PasswordNeverExpires $true
}
