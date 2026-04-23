rm -rf ./build
echo 'building'
pnpm build
echo 'uploading files'
rsync -a ./build root@107.152.45.68:/root/fia/
echo 'ssh-ing'
ssh root@107.152.45.68 'systemctl restart fia'
echo 'deployment finished'