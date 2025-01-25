import streamlit as st
import pandas as pd
import io

# Streamlit app
def main():
    st.title("CSV to Parquet Converter")
    st.write("Upload a CSV file, and it will be converted to a Parquet file!")

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

if __name__ == "__main__":
    main()