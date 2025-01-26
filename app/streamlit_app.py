import streamlit as st
import pandas as pd
import pyarrow.parquet as pq
import io
import os

# function to convert bytes to Megabytes MB
def format_size_kb_mb(size_in_bytes):
    """Convert bytes to KB or MB, depending on size."""
    if size_in_bytes < 1024 * 1024:  # Less than 1 MB
        return f"{size_in_bytes / 1024:.2f} KB"
    else:
        return f"{size_in_bytes / (1024 * 1024):.2f} MB"

# Streamlit main app
def main():
    st.title("Parqueology")

    # Tabs
    tab1, tab2 = st.tabs(["CSV to Parquet Converter", "Parquet File Viewer"])

    with tab1:
        st.subheader("Upload a CSV file and get it in Parquet!")

        # File uploader
        uploaded_file = st.file_uploader(" ", type = "csv")

        if uploaded_file is not None:
            #Display a preview of the uploaded CSV
            df = pd.read_csv(uploaded_file)
            st.write("Preview of uploaded CSV:")
            st.dataframe(df.head())

            # Output parquet file name
            parquet_filename = uploaded_file.name.replace(".csv",".parquet")

            # Button to trigger the conversion
            if st.button("Convert to Parquet"):
                
                # Convert the dataframe to parquet using in-memory buffer (BytesIO), suitable for small files (<100MB)
                buffer = io.BytesIO()
                df.to_parquet(parquet_filename, engine='pyarrow')
                # Reset pointer to the beginning of the buffer
                buffer.seek(0)
            
                # Display the result message
                st.write(f"Successfully converted to {parquet_filename}")
                
                # Provide a download link for the parquet file
                st.download_button(
                    label = "Dowlnload Parquet File",
                    data=buffer,
                    file_name=parquet_filename,
                    mime="application/octet-stream"
                )

    with tab2:
        preview_rows = 20
        st.subheader("Inspect Parquet Files: Metadata and Data Preview")


        # File uploader for Parquet file
        uploaded_parquet = st.file_uploader("Upload your Parquet file", type="parquet")

        #Preview the first rows of the parquet file
        if uploaded_parquet is not None:
            # Data Frame
            df = pd.read_parquet(uploaded_parquet)

            # Retrieve metadata using pyarrow.parquet
            pq_object = pq.ParquetFile(uploaded_parquet)
            num_rows = pq_object.metadata.num_rows
            num_columns = pq_object.metadata.num_columns
            compression_type = pq_object.metadata.row_group(0).column(0).compression
            metadata = pq_object.metadata
            
            # Get the total file size
            uploaded_parquet.seek(0, os.SEEK_END)  # Move to the end of the file
            total_file_size = uploaded_parquet.tell()  # Get the file size in bytes
            uploaded_parquet.seek(0)  # Reset the file pointer to the beginning

            # Calculate data payload size (total size - metadata size)
            data_payload_size = total_file_size - metadata.serialized_size


            # Combine basic and detailed metadata into a single dictionary
            combined_metadata = {
                "File Name": uploaded_parquet.name,
                "Total File Size": format_size_kb_mb(total_file_size),
                "MetaData Size": format_size_kb_mb(metadata.serialized_size),
                "Data Payload Size": format_size_kb_mb(data_payload_size),
                "Number of Columns": num_columns,
                "Number of Rows": num_rows,
                "Compression Type": compression_type,
                "Parquet Format Version": metadata.format_version,
                "Created By": metadata.created_by,
            }

            # Display the combined metadata in a single table
            st.subheader("Metadata")
            st.table(pd.DataFrame(list(combined_metadata.items()), columns=["Attribute", "Value"]))


            # Display schema information
            st.subheader("Schema Information")
            schema = pq_object.schema.to_arrow_schema()  # Convert Parquet schema to Arrow schema
            schema_fields = []
            for field in schema:
                schema_fields.append({
                    "Column Name": field.name,
                    "Data Type": str(field.type),  # Use field.type for Arrow schema
                    "Nullable": field.nullable,    # Use field.nullable for Arrow schema
                })
            st.table(pd.DataFrame(schema_fields))

    
            # Display a preview of the data
            st.subheader(f"Preview of the First {preview_rows} Rows")
            st.dataframe(df.head(preview_rows))


if __name__ == "__main__":
    main()