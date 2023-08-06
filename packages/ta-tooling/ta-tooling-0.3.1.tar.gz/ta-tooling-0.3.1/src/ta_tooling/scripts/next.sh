# While grading this function can be used to quickly move to the
# folder of the next student.
#
# AKA change from
#     cd ../ && cd next-student-folder
# to
#     next
#
# Technically, it looks up the name of the current
# folder. The function then list all sub-directory of
# the parent directory. The linear serach is used until
# the current folder is found. The script then cd to the
# folder after the current folder is found.
function next() {
    current_name=${PWD##*/}
    is_found="0"

    for name in $(find ../ -maxdepth 1 -type d -printf '%f\n' | grep -E '[a-z]{2}[0-9]{6}' | sort)
    do
        if [[ "$name" == "$current_name" ]]; then
            is_found="1"
            continue
        fi

        if [[ "$is_found" == "1" ]]; then
            cd "../$name"
            break
        fi
    done
}
