#!/bin/bash 
## mk kmer table from count files

input_files=("${@:1:$(($#-1))}")
output_file="${!#}"

## debug
# define function for multiple join
joinm() {
    f1=$1; f2=$2; shift 2;

    # Create temporary files to hold decompressed data
    tmp1=$(mktemp)
    tmp2=$(mktemp)

    # Decompress files to temporary files
    if [[ "$f1" == *.gz ]]; then
        zcat "$f1" | sort > "$tmp1"
        f1="$tmp1"
    fi

    if [[ "$f2" == *.gz ]]; then
        zcat "$f2" | sort > "$tmp2"
        f2="$tmp2"
    fi

    if [ $# -gt 0 ]
    then
        # join files
        join -a 1 -a 2 -e 0 "$f1" "$f2" -o auto -t $'\t' | joinm - "$@"

    else
        # join 2 files
        join -a 1 -a 2 -e 0 "$f1" "$f2" -o auto -t $'\t'

    fi

    # Clean up temporary files
    rm -f "$tmp1" "$tmp2"
}

## merge files
joinm "${input_files[@]}" > out.tmp

## construct header
HEADER=$(echo "mer")

## Construct header
HEADER="mer"
for file in "${input_files[@]}"; do
    NAME=$(basename "$file" | cut -d. -f1)
    HEADER="${HEADER}\t${NAME}"
done

# add header to file
sed '1s/^/'"$HEADER"'\n/' out.tmp | gzip > "$output_file"
