version_compare() {
    local ver1="${1#V}"  # Убираем "V" из первой версии
    local ver2="${2#V}"  # Убираем "V" из второй версии

    # Удаляем суффикс после "__"
    ver1="${ver1%%__*}"
    ver2="${ver2%%__*}"

    # Разбиваем версии на части по точке
    IFS='.' read -r -a ver1_parts <<< "${ver1//-/.}"
    IFS='.' read -r -a ver2_parts <<< "${ver2//-/.}"

    # Сравниваем каждую часть версии
    for i in {0..2}; do
        if (( 10#${ver1_parts[i]} < 10#${ver2_parts[i]} )); then
            return 0
        elif (( 10#${ver1_parts[i]} > 10#${ver2_parts[i]} )); then
            return 1
        fi
    done

    # Если числа одинаковые, сравниваем строковые части
    local alpha1="${ver1_parts[3]}"
    local alpha2="${ver2_parts[3]}"

    if [[ "$alpha1" < "$alpha2" ]]; then
        return 0
    elif [[ "$alpha1" > "$alpha2" ]]; then
        return 1
    fi

    # Если все части равны, версии равны
    return 0
}

 if [ "$MIGRATION_VERSION" == "latest" ]; then
    # Выполнить все миграции
    for migration_script in $(ls /migrations/V*.{sql,sh} | sort -V); do
        psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "$migration_script"
    done
else
    # Выполнить миграции до указанной версии
    for migration_script in $(ls /migrations/V*.{sql,sh} | sort -V); do
        version=$(basename "$migration_script" | sed 's/^V//')
        if version_compare "$version" "$MIGRATION_VERSION"; then
            psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "$migration_script"
        fi
    done
fi