#!/bin/bash

# USAGE
# =====
# bash api_sanity.sh.sh health      ->  Check API health
# bash api_sanity.sh.sh ping        ->  Ping API
# bash api_sanity.sh.sh list        ->  List all memcells
# bash api_sanity.sh.sh create      ->  Create a new memcell
# bash api_sanity.sh.sh get <ID>    ->  Get a specific memcell
# bash api_sanity.sh.sh update <ID> ->  Update a specific memcell
# bash api_sanity.sh.sh delete <ID> ->  Delete a specific memcell

# Set the base URL of your Flask API
BASE_URL="http://localhost:5000"

# check if online
check_health() {
    echo "Checking API health..."
    curl -s "${BASE_URL}/" | jq .
    echo
}

# ping API
ping_api() {
    echo "Pinging API..."
    curl -s "${BASE_URL}/ping" | jq .
    echo
}

# get all memcells
get_all_memcells() {
    echo "Fetching all memcells..."
    curl -s "${BASE_URL}/memcells" | jq .
    echo
}

# create a new memcell
create_memcell() {
    echo "Creating a new memcell..."
    curl -s -X POST "${BASE_URL}/memcells" \
        -H "Content-Type: application/json" \
        -d '{
            "phone": "+1234567890",
            "task": "Test task"
        }' | jq .
    echo
}

# get a specific memcell by ID
get_memcell() {
    local mem_id=$1
    if [ -z "$mem_id" ]; then
        echo "Error: You must provide a memcell ID."
        return
    fi
    echo "Fetching memcell with ID: ${mem_id}..."
    curl -s "${BASE_URL}/memcells/${mem_id}" | jq .
    echo
}

# delete a memcell by ID
delete_memcell() {
    local mem_id=$1
    if [ -z "$mem_id" ]; then
        echo "Error: You must provide a memcell ID."
        return
    fi
    echo "Deleting memcell with ID: ${mem_id}..."
    curl -s -X DELETE "${BASE_URL}/memcells/${mem_id}" | jq .
    echo
}

# update a memcell by ID
update_memcell() {
    local mem_id=$1
    if [ -z "$mem_id" ]; then
        echo "Error: You must provide a memcell ID."
        return
    fi
    echo "Updating memcell with ID: ${mem_id}..."
    curl -s -X PUT "${BASE_URL}/memcells/${mem_id}" \
        -H "Content-Type: application/json" \
        -d '{
            "task": "Updated task description"
        }' | jq .
    echo
}

# if arguments are passed, run directly
if [ $# -gt 0 ]; then
    case $1 in
        health) check_health ;;
        ping) ping_api ;;
        list) get_all_memcells ;;
        create) create_memcell ;;
        get) get_memcell $2 ;;
        update) update_memcell $2 ;;
        delete) delete_memcell $2 ;;
        *)
            echo "Invalid option. Usage:"
            echo "bash api_sanity.sh.sh [health|ping|list|create|get|update|delete] [ID (for get/update/delete)]"
            ;;
    esac
    exit 0
fi

# interactive menu 
# (if no arguments)
while true; do
    echo "API SANITY CHECKS"
    echo "-----------------------"
    echo "1. Check API Health"
    echo "2. Ping API"
    echo "3. Get All Memcells"
    echo "4. Create New Memcell"
    echo "5. Get Specific Memcell"
    echo "6. Update Memcell"
    echo "7. Delete Memcell"
    echo "8. Exit"
    echo
    read -p "Choose an option: " choice

    case $choice in
        1) check_health ;;
        2) ping_api ;;
        3) get_all_memcells ;;
        4) create_memcell ;;
        5) 
            read -p "Enter Memcell ID: " mem_id
            get_memcell $mem_id 
            ;;
        6) 
            read -p "Enter Memcell ID to update: " mem_id
            update_memcell $mem_id 
            ;;
        7) 
            read -p "Enter Memcell ID to delete: " mem_id
            delete_memcell $mem_id 
            ;;
        8) 
            echo "Exiting..."
            exit 0 
            ;;
        *) 
            echo "Invalid option. Please choose again."
            ;;
    esac
    echo
done
