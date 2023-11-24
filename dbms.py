import streamlit as st
import pymysql
import pandas as pd

# Create a function to establish a database connection
def create_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='rhtx@sql',
        database='militarydb'
    )

def get_table_data(table_name):
    connection = create_db_connection()
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df

# Create a Streamlit app
st.title("Firearm Military Database")

# Choose a table for CRUD operations
selected_table = st.selectbox("Select a table", ["Firearm", "MaintenanceRecord", "Soldier",
                                                                  "FirearmAccessories", "Armory", "TrainingExercise",
                                                                  "Ammunition", "AmmunitionLot", "MaintenanceItem"])


if selected_table == "Firearm":
    st.header("View Firearm Data")
    firearm_data = get_table_data("Firearm")
    st.dataframe(firearm_data)

    operation = st.radio("Select Operation", ["Add", "Update", "Delete"])

    if operation == "Add":
        # Add a new firearm
        st.header("Add a New Firearm")
        serial_number = st.text_input("Serial Number")
        make = st.text_input("Make")
        model = st.text_input("Model")
        caliber = st.text_input("Caliber")
        weight = st.number_input("Weight", 0.0, 1000.0)
        status = st.text_input("Status")
        if st.button("Add Firearm"):
            connection = create_db_connection()
            cursor = connection.cursor()
            insert_query = f"INSERT INTO Firearm (SerialNumber, Make, Model, Caliber, Weight, Status) " \
                        f"VALUES ('{serial_number}', '{make}', '{model}', '{caliber}', {weight}, '{status}');"
            cursor.execute(insert_query)
            connection.commit()
            connection.close()
            st.success("Firearm added successfully.")


    elif operation == "Update":
        st.header("Update Firearm Data")
        selected_serial_number_update = st.selectbox("Select Serial Number to Update", firearm_data['SerialNumber'])
        new_make = st.text_input("New Make")
        new_model = st.text_input("New Model")
        new_caliber = st.text_input("New Caliber")
        new_weight = st.number_input("New Weight", 0.0, 1000.0)
        new_status = st.text_input("New Status")
        if st.button("Update Firearm"):
            connection = create_db_connection()
            cursor = connection.cursor()
            update_query = f"UPDATE Firearm " \
                           f"SET Make = '{new_make}', Model = '{new_model}', " \
                           f"Caliber = '{new_caliber}', Weight = {new_weight}, Status = '{new_status}' " \
                           f"WHERE SerialNumber = {selected_serial_number_update};"
            cursor.execute(update_query)
            connection.commit()
            connection.close()
            st.success("Firearm updated successfully.")
            st.experimental_rerun()

    elif operation == "Delete":
        st.header("Delete Firearm")
        serial_number_to_delete = st.text_input("Enter Serial Number to Delete")
        if st.button("Delete Firearm"):
            if serial_number_to_delete:
                connection = create_db_connection()
                cursor = connection.cursor()
                delete_query = f"DELETE FROM Firearm WHERE SerialNumber = '{serial_number_to_delete}';"
                cursor.execute(delete_query)
                connection.commit()
                connection.close()
                st.success(f"Firearm with Serial Number {serial_number_to_delete} deleted successfully.")
                st.experimental_rerun()
            else:
                st.warning("Please enter a Serial Number to delete.")





elif selected_table == "MaintenanceRecord":
    st.header("View MaintenanceRecord Data")
    maintenance_data = get_table_data("MaintenanceRecord")
    st.dataframe(maintenance_data)

    # Get firearm data
    firearm_data = get_table_data("Firearm")

    # Add a new maintenance record
   
    # Add a new maintenance record
    st.header("Add a New Maintenance Record")
    # Query the Firearm table to get available SerialNumber options
    firearm_data = get_table_data("Firearm")
    selected_firearm_serial_number = st.selectbox("Firearm Serial Number", firearm_data['SerialNumber'])
    date_of_maintenance = st.date_input("Date of Maintenance")
    maintenance_type = st.text_input("Type")
    description = st.text_input("Description")
    maintenance_cost = st.number_input("Maintenance Cost", 0.0, 10000.0)
    if st.button("Add Maintenance Record"):
        connection = create_db_connection()
        cursor = connection.cursor()
        insert_query = f"INSERT INTO MaintenanceRecord (FirearmSerialNumber, DateOfMaintenance, Type, Description, MaintenanceCost) " \
                    f"VALUES ({selected_firearm_serial_number}, '{date_of_maintenance}', '{maintenance_type}', '{description}', {maintenance_cost});"
        cursor.execute(insert_query)
        connection.commit()
        connection.close()
        st.success("Maintenance Record added successfully.")


    # Update a maintenance record
    st.header("Update Maintenance Record Data")
    selected_record_id_update = st.selectbox("Select Maintenance Record ID to Update", maintenance_data['MaintenanceRecordID'])
    new_firearm_serial_number = st.selectbox("New Firearm Serial Number", firearm_data['SerialNumber'])
    new_date_of_maintenance = st.date_input("New Date of Maintenance")
    new_maintenance_type = st.text_input("New Type")
    new_description = st.text_input("New Description")
    new_maintenance_cost = st.number_input("New Maintenance Cost", 0.0, 10000.0)
    if st.button("Update Maintenance Record"):
        connection = create_db_connection()
        cursor = connection.cursor()
        update_query = f"UPDATE MaintenanceRecord " \
                       f"SET FirearmSerialNumber = {new_firearm_serial_number}, " \
                       f"DateOfMaintenance = '{new_date_of_maintenance}', " \
                       f"Type = '{new_maintenance_type}', " \
                       f"Description = '{new_description}', " \
                       f"MaintenanceCost = {new_maintenance_cost} " \
                       f"WHERE MaintenanceRecordID = {selected_record_id_update};"
        cursor.execute(update_query)
        connection.commit()
        connection.close()
        st.success("Maintenance Record updated successfully.")

    # Delete a maintenance record
    st.header("Delete Maintenance Record")
    selected_record_id_delete = st.selectbox("Select Maintenance Record ID to Delete", maintenance_data['MaintenanceRecordID'])
    if st.button("Delete Maintenance Record"):
        connection = create_db_connection()
        cursor = connection.cursor()
        delete_query = f"DELETE FROM MaintenanceRecord WHERE MaintenanceRecordID = {selected_record_id_delete};"
        cursor.execute(delete_query)
        connection.commit()
        connection.close()
        st.success("Maintenance Record deleted successfully.")

elif selected_table == "Soldier":
    st.header("View Soldier Data")
    soldier_data = get_table_data("Soldier")
    st.dataframe(soldier_data)

    # Add a new soldier
    st.header("Add a New Soldier")
    soldier_rank = st.text_input("Rank")
    name = st.text_input("Name")
    date_of_birth = st.date_input("Date of Birth")
    unit = st.text_input("Unit")
    duty_status = st.text_input("Duty Status")
    if st.button("Add Soldier"):
        connection = create_db_connection()
        cursor = connection.cursor()
        insert_query = f"INSERT INTO Soldier (SoldierRank, Name, DateOfBirth, Unit, DutyStatus) " \
                       f"VALUES ('{soldier_rank}', '{name}', '{date_of_birth}', '{unit}', '{duty_status}');"
        cursor.execute(insert_query)
        connection.commit()
        connection.close()
        st.success("Soldier added successfully.")

    # Update a soldier
    st.header("Update Soldier Data")
    selected_soldier_id_update = st.selectbox("Select Soldier ID to Update", soldier_data['SoldierID'])
    new_soldier_rank = st.text_input("New Rank")
    new_name = st.text_input("New Name")
    new_date_of_birth = st.date_input("New Date of Birth")
    new_unit = st.text_input("New Unit")
    new_duty_status = st.text_input("New Duty Status")
    if st.button("Update Soldier"):
        connection = create_db_connection()
        cursor = connection.cursor()
        update_query = f"UPDATE Soldier " \
                       f"SET SoldierRank = '{new_soldier_rank}', Name = '{new_name}', " \
                       f"DateOfBirth = '{new_date_of_birth}', Unit = '{new_unit}', DutyStatus = '{new_duty_status}' " \
                       f"WHERE SoldierID = '{selected_soldier_id_update}';"
        cursor.execute(update_query)
        connection.commit()
        connection.close()
        st.success("Soldier updated successfully.")

    # Delete a soldier
    st.header("Delete Soldier")
    selected_soldier_id_delete = st.selectbox("Select Soldier ID to Delete", soldier_data['SoldierID'])
    if st.button("Delete Soldier"):
        connection = create_db_connection()
        cursor = connection.cursor()
        delete_query = f"DELETE FROM Soldier WHERE SoldierID = '{selected_soldier_id_delete}';"
        cursor.execute(delete_query)
        connection.commit()
        connection.close()
        st.success("Soldier deleted successfully.")

# Add CRUD operations for FirearmAccessories
elif selected_table == "FirearmAccessories":
    st.header("View Firearm Accessories Data")
    firearm_accessories_data = get_table_data("FirearmAccessories")
    st.dataframe(firearm_accessories_data)

    # Add a new firearm accessory
    firearm_data = get_table_data("Firearm")
    firearm_serial_number = st.selectbox("Firearm Serial Number", firearm_data['SerialNumber'])
    accessory_type = st.text_input("Accessory Type")
    manufacturer = st.text_input("Manufacturer")
    model = st.text_input("Model")
    compatibility = st.text_input("Compatibility")
    quantity_in_stock = st.number_input("Quantity in Stock", 0, 10000)
    if st.button("Add Firearm Accessory"):
        connection = create_db_connection()
        cursor = connection.cursor()
        insert_query = f"INSERT INTO FirearmAccessories (FirearmSerialNumber, AccessoryType, Manufacturer, Model, Compatibility, QuantityInStock) " \
                       f"VALUES ({firearm_serial_number}, '{accessory_type}', '{manufacturer}', '{model}', '{compatibility}', {quantity_in_stock});"
        cursor.execute(insert_query)
        connection.commit()
        connection.close()
        st.success("Firearm Accessory added successfully.")

    # Update a firearm accessory
    st.header("Update Firearm Accessory Data")
    selected_accessory_id_update = st.selectbox("Select Accessory ID to Update", firearm_accessories_data['AccessoryID'])
    new_firearm_serial_number = st.selectbox("New Firearm Serial Number", firearm_data['SerialNumber'])
    new_accessory_type = st.text_input("New Accessory Type")
    new_manufacturer = st.text_input("New Manufacturer")
    new_model = st.text_input("New Model")
    new_compatibility = st.text_input("New Compatibility")
    new_quantity_in_stock = st.number_input("New Quantity in Stock", 0, 10000)
    if st.button("Update Firearm Accessory"):
        connection = create_db_connection()
        cursor = connection.cursor()
        update_query = f"UPDATE FirearmAccessories " \
                       f"SET FirearmSerialNumber = {new_firearm_serial_number}, AccessoryType = '{new_accessory_type}', " \
                       f"Manufacturer = '{new_manufacturer}', Model = '{new_model}', Compatibility = '{new_compatibility}', " \
                       f"QuantityInStock = {new_quantity_in_stock} " \
                       f"WHERE AccessoryID = {selected_accessory_id_update};"
        cursor.execute(update_query)
        connection.commit()
        connection.close()
        st.success("Firearm Accessory updated successfully.")

    # Delete a firearm accessory
    st.header("Delete Firearm Accessory")
    selected_accessory_id_delete = st.selectbox("Select Accessory ID to Delete", firearm_accessories_data['AccessoryID'])
    if st.button("Delete Firearm Accessory"):
        connection = create_db_connection()
        cursor = connection.cursor()
        delete_query = f"DELETE FROM FirearmAccessories WHERE AccessoryID = {selected_accessory_id_delete};"
        cursor.execute(delete_query)
        connection.commit()
        connection.close()
        st.success("Firearm Accessory deleted successfully.")

# Add CRUD operations for Armory
elif selected_table == "Armory":
    st.header("View Armory Data")
    armory_data = get_table_data("Armory")
    st.dataframe(armory_data)

    # Add a new armory entry
    st.header("Add a New Armory Entry")
    location = st.text_input("Location")
    capacity = st.number_input("Capacity", 0, 10000)
    armorer_in_charge = st.text_input("Armorer in Charge")
    security_level = st.text_input("Security Level")
    surveillance_cameras = st.text_input("Surveillance Cameras")
    if st.button("Add Armory Entry"):
        connection = create_db_connection()
        cursor = connection.cursor()
        insert_query = f"INSERT INTO Armory (Location, Capacity, ArmorerInCharge, SecurityLevel, SurveillanceCameras) " \
                       f"VALUES ('{location}', {capacity}, '{armorer_in_charge}', '{security_level}', '{surveillance_cameras}');"
        cursor.execute(insert_query)
        connection.commit()
        connection.close()
        st.success("Armory entry added successfully.")

    # Update an armory entry
    st.header("Update Armory Entry Data")
    selected_armory_id_update = st.selectbox("Select Armory ID to Update", armory_data['ArmoryID'])
    new_location = st.text_input("New Location")
    new_capacity = st.number_input("New Capacity", 0, 10000)
    new_armorer_in_charge = st.text_input("New Armorer in Charge")
    new_security_level = st.text_input("New Security Level")
    new_surveillance_cameras = st.text_input("New Surveillance Cameras")
    if st.button("Update Armory Entry"):
        connection = create_db_connection()
        cursor = connection.cursor()
        update_query = f"UPDATE Armory " \
                       f"SET Location = '{new_location}', Capacity = {new_capacity}, " \
                       f"ArmorerInCharge = '{new_armorer_in_charge}', SecurityLevel = '{new_security_level}', " \
                       f"SurveillanceCameras = '{new_surveillance_cameras}' " \
                       f"WHERE ArmoryID = {selected_armory_id_update};"
        cursor.execute(update_query)
        connection.commit()
        connection.close()
        st.success("Armory entry updated successfully.")

    # Delete an armory entry
    st.header("Delete Armory Entry")
    selected_armory_id_delete = st.selectbox("Select Armory ID to Delete", armory_data['ArmoryID'])
    if st.button("Delete Armory Entry"):
        connection = create_db_connection()
        cursor = connection.cursor()
        delete_query = f"DELETE FROM Armory WHERE ArmoryID = {selected_armory_id_delete};"
        cursor.execute(delete_query)
        connection.commit()
        connection.close()
        st.success("Armory entry deleted successfully.")

# Add CRUD operations for TrainingExercise
elif selected_table == "TrainingExercise":
    st.header("View Training Exercise Data")
    training_exercise_data = get_table_data("TrainingExercise")
    st.dataframe(training_exercise_data)

    # Add a new training exercise
    st.header("Add a New Training Exercise")
    exercise_name = st.text_input("Exercise Name")
    date = st.date_input("Date")
    description = st.text_input("Description")
    duration = st.number_input("Duration (hours)", 0, 1000)
    weather_conditions = st.text_input("Weather Conditions")
    training_type = st.text_input("Training Type")
    if st.button("Add Training Exercise"):
        connection = create_db_connection()
        cursor = connection.cursor()
        insert_query = f"INSERT INTO TrainingExercise (ExerciseName, Date, Description, Duration, WeatherConditions, TrainingType) " \
                       f"VALUES ('{exercise_name}', '{date}', '{description}', {duration}, '{weather_conditions}', '{training_type}');"
        cursor.execute(insert_query)
        connection.commit()
        connection.close()
        st.success("Training Exercise added successfully.")

    # Update a training exercise
    st.header("Update Training Exercise Data")
    selected_exercise_id_update = st.selectbox("Select Exercise ID to Update", training_exercise_data['ExerciseID'])
    new_exercise_name = st.text_input("New Exercise Name")
    new_date = st.date_input("New Date")
    new_description = st.text_input("New Description")
    new_duration = st.number_input("New Duration (hours)", 0, 1000)
    new_weather_conditions = st.text_input("New Weather Conditions")
    new_training_type = st.text_input("New Training Type")
    if st.button("Update Training Exercise"):
        connection = create_db_connection()
        cursor = connection.cursor()
        update_query = f"UPDATE TrainingExercise " \
                       f"SET ExerciseName = '{new_exercise_name}', Date = '{new_date}', " \
                       f"Description = '{new_description}', Duration = {new_duration}, " \
                       f"WeatherConditions = '{new_weather_conditions}', TrainingType = '{new_training_type}' " \
                       f"WHERE ExerciseID = {selected_exercise_id_update};"
        cursor.execute(update_query)
        connection.commit()
        connection.close()
        st.success("Training Exercise updated successfully.")

    # Delete a training exercise
    st.header("Delete Training Exercise")
    selected_exercise_id_delete = st.selectbox("Select Exercise ID to Delete", training_exercise_data['ExerciseID'])
    if st.button("Delete Training Exercise"):
        connection = create_db_connection()
        cursor = connection.cursor()
        delete_query = f"DELETE FROM TrainingExercise WHERE ExerciseID = {selected_exercise_id_delete};"
        cursor.execute(delete_query)
        connection.commit()
        connection.close()
        st.success("Training Exercise deleted successfully.")

# Add CRUD operations for Ammunition
elif selected_table == "Ammunition":
    st.header("View Ammunition Data")
    ammunition_data = get_table_data("Ammunition")
    st.dataframe(ammunition_data)

    # Add a new ammunition entry
    st.header("Add a New Ammunition Entry")
    caliber = st.text_input("Caliber")
    quantity_in_stock = st.number_input("Quantity in Stock", 0, 10000)
    manufacturer = st.text_input("Manufacturer")
    date_of_acquisition = st.date_input("Date of Acquisition")
    ammo_type = st.text_input("Ammo Type")
    if st.button("Add Ammunition Entry"):
        connection = create_db_connection()
        cursor = connection.cursor()
        insert_query = f"INSERT INTO Ammunition (Caliber, QuantityInStock, Manufacturer, DateOfAcquisition, Type) " \
                       f"VALUES ('{caliber}', {quantity_in_stock}, '{manufacturer}', '{date_of_acquisition}', '{ammo_type}');"
        cursor.execute(insert_query)
        connection.commit()
        connection.close()
        st.success("Ammunition entry added successfully.")

    # Update an ammunition entry
    st.header("Update Ammunition Entry Data")
    selected_ammo_id_update = st.selectbox("Select Ammunition ID to Update", ammunition_data['AmmunitionID'])
    new_caliber = st.text_input("New Caliber")
    new_quantity_in_stock = st.number_input("New Quantity in Stock", 0, 10000)
    new_manufacturer = st.text_input("New Manufacturer")
    new_date_of_acquisition = st.date_input("New Date of Acquisition")
    new_ammo_type = st.text_input("New Ammo Type")
    if st.button("Update Ammunition Entry"):
        connection = create_db_connection()
        cursor = connection.cursor()
        update_query = f"UPDATE Ammunition " \
                       f"SET Caliber = '{new_caliber}', QuantityInStock = {new_quantity_in_stock}, " \
                       f"Manufacturer = '{new_manufacturer}', DateOfAcquisition = '{new_date_of_acquisition}', " \
                       f"Type = '{new_ammo_type}' " \
                       f"WHERE AmmunitionID = {selected_ammo_id_update};"
        cursor.execute(update_query)
        connection.commit()
        connection.close()
        st.success("Ammunition entry updated successfully.")

    # Delete an ammunition entry
    st.header("Delete Ammunition Entry")
    selected_ammo_id_delete = st.selectbox("Select Ammunition ID to Delete", ammunition_data['AmmunitionID'])
    if st.button("Delete Ammunition Entry"):
        connection = create_db_connection()
        cursor = connection.cursor()
        delete_query = f"DELETE FROM Ammunition WHERE AmmunitionID = {selected_ammo_id_delete};"
        cursor.execute(delete_query)
        connection.commit()
        connection.close()
        st.success("Ammunition entry deleted successfully.")

# Add CRUD operations for AmmunitionLot
elif selected_table == "AmmunitionLot":
    st.header("View Ammunition Lot Data")
    ammunition_lot_data = get_table_data("AmmunitionLot")
    st.dataframe(ammunition_lot_data)

    # Add a new ammunition lot
    st.header("Add a New Ammunition Lot")
    lot_number = st.text_input("Lot Number")
    ammunition_data = get_table_data("Ammunition")
    quantity_in_stock = st.number_input("Quantity in Stock", 0, 10000)
    date_of_manufacture = st.date_input("Date of Manufacture")
    ammo_id = st.selectbox("Ammunition ID", ammunition_data['AmmunitionID'])
    if st.button("Add Ammunition Lot"):
        connection = create_db_connection()
        cursor = connection.cursor()
        insert_query = f"INSERT INTO AmmunitionLot (LotNumber, QuantityInStock, DateOfManufacture, AmmunitionID) " \
                       f"VALUES ('{lot_number}', {quantity_in_stock}, '{date_of_manufacture}', {ammo_id});"
        cursor.execute(insert_query)
        connection.commit()
        connection.close()
        st.success("Ammunition Lot added successfully.")

    # Update an ammunition lot
    st.header("Update Ammunition Lot Data")
    selected_lot_id_update = st.selectbox("Select Lot ID to Update", ammunition_lot_data['AmmunitionLotID'])
    new_lot_number = st.text_input("New Lot Number")
    new_quantity_in_stock = st.number_input("New Quantity in Stock", 0, 10000)
    new_date_of_manufacture = st.date_input("New Date of Manufacture")
    new_ammo_id = st.selectbox("New Ammunition ID", ammunition_data['AmmunitionID'])
    if st.button("Update Ammunition Lot"):
        connection = create_db_connection()
        cursor = connection.cursor()
        update_query = f"UPDATE AmmunitionLot " \
                       f"SET LotNumber = '{new_lot_number}', QuantityInStock = {new_quantity_in_stock}, " \
                       f"DateOfManufacture = '{new_date_of_manufacture}', AmmunitionID = {new_ammo_id} " \
                       f"WHERE AmmunitionLotID = {selected_lot_id_update};"
        cursor.execute(update_query)
        connection.commit()
        connection.close()
        st.success("Ammunition Lot updated successfully.")

    # Delete an ammunition lot
    st.header("Delete Ammunition Lot")
    selected_lot_id_delete = st.selectbox("Select Lot ID to Delete", ammunition_lot_data['AmmunitionLotID'])
    if st.button("Delete Ammunition Lot"):
        connection = create_db_connection()
        cursor = connection.cursor()
        delete_query = f"DELETE FROM AmmunitionLot WHERE AmmunitionLotID = {selected_lot_id_delete};"
        cursor.execute(delete_query)
        connection.commit()
        connection.close()
        st.success("Ammunition Lot deleted successfully.")

# Add CRUD operations for MaintenanceItem
elif selected_table == "MaintenanceItem":
    st.header("View Maintenance Item Data")
    maintenance_item_data = get_table_data("MaintenanceItem")
    st.dataframe(maintenance_item_data)

    # Add a new maintenance item
    st.header("Add a New Maintenance Item")
    date_of_item = st.date_input("Date of Item")
    maintenance_data = get_table_data("MaintenanceRecord")
    description = st.text_input("Description")
    cost = st.number_input("Cost", 0.0, 10000.0)
    maintenance_record_id = st.selectbox("Maintenance Record ID", maintenance_data['MaintenanceRecordID'])
    if st.button("Add Maintenance Item"):
        connection = create_db_connection()
        cursor = connection.cursor()
        insert_query = f"INSERT INTO MaintenanceItem (DateOfItem, Description, Cost, MaintenanceRecordID) " \
                       f"VALUES ('{date_of_item}', '{description}', {cost}, {maintenance_record_id});"
        cursor.execute(insert_query)
        connection.commit()
        connection.close()
        st.success("Maintenance Item added successfully.")

    # Update a maintenance item
    st.header("Update Maintenance Item Data")
    selected_item_id_update = st.selectbox("Select Item ID to Update", maintenance_item_data['MaintenanceItemID'])
    new_date_of_item = st.date_input("New Date of Item")
    new_description = st.text_input("New Description")
    new_cost = st.number_input("New Cost", 0.0, 10000.0)
    new_maintenance_record_id = st.selectbox("New Maintenance Record ID", maintenance_data['MaintenanceRecordID'])
    if st.button("Update Maintenance Item"):
        connection = create_db_connection()
        cursor = connection.cursor()
        update_query = f"UPDATE MaintenanceItem " \
                       f"SET DateOfItem = '{new_date_of_item}', Description = '{new_description}', " \
                       f"Cost = {new_cost}, MaintenanceRecordID = {new_maintenance_record_id} " \
                       f"WHERE MaintenanceItemID = {selected_item_id_update};"
        cursor.execute(update_query)
        connection.commit()
        connection.close()
        st.success("Maintenance Item updated successfully.")

    # Delete a maintenance item
    st.header("Delete Maintenance Item")
    selected_item_id_delete = st.selectbox("Select Item ID to Delete", maintenance_item_data['MaintenanceItemID'])
    if st.button("Delete Maintenance Item"):
        connection = create_db_connection()
        cursor = connection.cursor()
        delete_query = f"DELETE FROM MaintenanceItem WHERE MaintenanceItemID = {selected_item_id_delete};"
        cursor.execute(delete_query)
        connection.commit()
        connection.close()
        st.success("Maintenance Item deleted successfully.")
