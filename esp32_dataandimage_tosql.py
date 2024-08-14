from flask import Flask, request, jsonify
import pyodbc
import os

app = Flask(__name__)

# Directory where files will be saved
UPLOAD_FOLDER = r'N:\Shop\scb_data_collection\fj_destructive_test_results\test_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the directory exists

# Database connection parameters
connection_string = r"Driver={ODBC Driver 17 for SQL Server};Server=192.168.120.19,1433\SCB-APP01\SQLEXPRESS;Database=scbiiotdevices;Trusted_Connection=yes;"

@app.route('/endpoint', methods=['POST'])
def handle_request():
    if request.content_type == 'application/json':
        # Handle JSON data
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No JSON data provided"}), 400

        try:
            # Extract values from the incoming JSON
            operator_first_name = data.get("operator_first_name")
            project_id = data.get("project_id")
            panel_id = data.get("panel_id")
            shift_id = data.get("shift_id")
            sample_date = data.get("sample_date")
            sample_time = data.get("sample_time")
            specie = data.get("specie")
            grade = data.get("grade")
            dimension = data.get("dimension")
            mc_right = data.get("mc_right")
            mc_left = data.get("mc_left")
            test_result = data.get("test_result")
            max_psi_reading = data.get("max_psi_reading")
            max_load_reading = data.get("max_load_reading")
            wood_failure_mode = data.get("wood_failure_mode")
            min_ft_psi = data.get("min_ft_psi")
            fifth_ft_psi = data.get("fifth_ft_psi")
            min_uts_lbs = data.get("min_uts_lbs")
            fifth_uts_lbs = data.get("fifth_uts_lbs")
            adhesive_application = data.get("adhesive_application")
            squeeze_out = data.get("squeeze_out")
            adhesive_batch_test_result = data.get("adhesive_batch_test_result")
            finished_joint_appearance = data.get("finished_joint_appearance")
            positioning_alignment = data.get("positioning_alignment")

            # Establish the connection
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()

            # Query to get the device_id for the specified device_name
            device_name = "FJ Destructive Test Device"
            device_query = "SELECT device_id FROM Device WHERE device_name = ?"
            cursor.execute(device_query, (device_name,))
            device_result = cursor.fetchone()

            if device_result:
                device_id = device_result.device_id

                # Define the SQL INSERT statement with placeholders
                insert_query = '''
                INSERT INTO SampleResult (
                    device_id, operator_first_name, project_id, panel_id, shift_id, sample_date, sample_time, specie, grade, dimension,
                    mc_right, mc_left, test_result, max_psi_reading, max_load_reading, wood_failure_mode, min_ft_psi,
                    fifth_ft_psi, min_uts_lbs, fifth_uts_lbs, adhesive_application, squeeze_out, adhesive_batch_test_result,
                    finished_joint_appearance, positioning_alignment
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''

                # Define the values to be inserted
                values = (
                    device_id, operator_first_name, project_id, panel_id, shift_id, sample_date, sample_time, specie, grade, dimension,
                    mc_right, mc_left, test_result, max_psi_reading, max_load_reading, wood_failure_mode, min_ft_psi,
                    fifth_ft_psi, min_uts_lbs, fifth_uts_lbs, adhesive_application, squeeze_out, adhesive_batch_test_result,
                    finished_joint_appearance, positioning_alignment
                )

                # Ensure that the number of values matches the number of placeholders (25)
                if len(values) == 25:
                    # Execute the query
                    cursor.execute(insert_query, values)

                    # Commit the transaction
                    conn.commit()

                    # Retrieve the last inserted test_id based on created_at
                    cursor.execute('''
                    SELECT TOP 1 test_id
                    FROM SampleResult
                    ORDER BY created_at DESC
                    ''')
                    last_id_result = cursor.fetchone()
                    last_test_id = last_id_result.test_id if last_id_result else None

                    # Close the connection
                    cursor.close()
                    conn.close()

                    response = {
                        "status": "success",
                        "message": "Data inserted successfully!",
                        "test_id": last_test_id
                    }

                    # Print the test_id
                    print(f"Last inserted test_id: {last_test_id}")

                else:
                    response = {
                        "status": "error",
                        "message": "Mismatch between number of values and placeholders."
                    }
            else:
                response = {
                    "status": "error",
                    "message": f"Device with name '{device_name}' not found."
                }
        except Exception as e:
            response = {
                "status": "error",
                "message": f"An error occurred: {e}"
            }

        return jsonify(response), 200

    elif request.content_type.startswith('multipart/form-data'):
        # Handle file uploads
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file part in the request"}), 400

        files = request.files.getlist('file')  # Get list of files from the request

        # Ensure at least two files are received
        if len(files) < 2:
            return jsonify({"status": "error", "message": "Expected two files but received less"}), 400

        try:
            # Establish the database connection
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()
            print("Connection successful.")

            # Fetch the most recent test_id from the SampleResult table
            cursor.execute("SELECT test_id FROM SampleResult ORDER BY created_at DESC")
            row = cursor.fetchone()

            if row:
                test_id = row.test_id
                print(f"Most recent test_id: {test_id}")
            else:
                print("No records found in SampleResult table.")
                return jsonify({"status": "error", "message": "No records found in SampleResult table"}), 404

            file_names = []
            for file in files:
                if file.filename == '':
                    continue
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)  # Define the file path
                file.save(file_path)  # Save the file
                file_names.append(file.filename)

                # Insert file details into the Image table
                cursor.execute('''
                    INSERT INTO Image (test_id, filename, filepath) VALUES (?, ?, ?)
                ''', (test_id, file.filename, file_path))
                print(f"Inserted details for {file.filename} into Image table.")

            # Fetch image details for renaming
            cursor.execute('''
                SELECT image_id, filename FROM Image WHERE test_id = ?
            ''', (test_id,))
            images = cursor.fetchall()

            for image in images:
                image_id, filename = image
                new_filename = f"{image_id}_{filename}"  # Create new filename
                old_path = os.path.join(UPLOAD_FOLDER, filename)
                new_path = os.path.join(UPLOAD_FOLDER, new_filename)
                os.rename(old_path, new_path)  # Rename the file
                
                # Update file path in the Image table
                cursor.execute('''
                    UPDATE Image SET filename = ?, filepath = ? WHERE image_id = ?
                ''', (new_filename, new_path, image_id))
                print(f"Renamed file to {new_filename} and updated in Image table.")

            # Commit the transactions
            conn.commit()
            print("Image details updated successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({"status": "error", "message": f"An error occurred: {e}"}), 500

        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()

        return jsonify({"status": "success", "message": f"Files uploaded and processed successfully: {', '.join(file_names)}"}), 200

    else:
        return jsonify({"error": "Unsupported Media Type"}), 415

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
