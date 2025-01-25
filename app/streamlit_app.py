import streamlit as st
import pandas as pd
import pyarrow.parquet as pq
import io

# Streamlit app
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
        st.subheader(f"View the first {preview_rows} rows of any Parquet file..")

        # File uploader for Parquet file
        uploaded_parquet = st.file_uploader("Upload your Parquet file", type="parquet")

        #Preview the first rows of the parquet file
        if uploaded_parquet is not None:
            # Data Frame
            df = pd.read_parquet(uploaded_parquet)

            # Properties using pyarrow.parquet
            pq_object = pq.ParquetFile(uploaded_parquet)
            num_rows = pq_object.metadata.num_rows
            num_columns = pq_object.metadata.num_columns
            compression_type = pq_object.metadata.row_group(0).column(0).compression
            metadata = pq_object.metadata


            st.write(f"{uploaded_parquet.name} has {num_columns} columns and {num_rows} rows.")
            st.write(f"Compression Type: {compression_type}")

            st.write(f"metadata: {metadata}")

    

            st.write(f"Here's how the first {preview_rows} rows look:")
            st.dataframe(df.head(preview_rows))


if __name__ == "__main__":
    main()