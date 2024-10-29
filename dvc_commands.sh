#!/bin/bash

source /home/mostafa/Desktop/FSD\ Projects/big_mart/.env
version=$VERSION

increment_version() {
    major=${version%%.*}
    minor=${version##*.} 
    if [ "$minor" -eq 9 ]; then
        major=$((major + 1))
        minor=0
    else
        minor=$((minor + 1))
    fi
    echo "$major.$minor"
}

new_version=$(increment_version)

sed -i "s/VERSION=$version/VERSION=$new_version/" /home/mostafa/Desktop/FSD\ Projects/big_mart/.env

cd '/home/mostafa/Desktop/FSD Projects/big_mart'
dvc add dags/data/dvc_df.csv
dvc add dags/data/df.csv
git add .
git commit -m "add data version $new_version"
git tag -a "v$new_version" -m "Version $new_version"
dvc push
git push
git push origin --tags

echo "---- Done: Version $new_version ----"
