import pandas as pd


AD = {
    "id":"id",
    "Integrity":"integritynumber",
    "Range":"sizerange",
    "Size":"averagesizeinrange",
    "Conc":"concentrationinrange",
    "Molarity":"concentrationmolarinrange",
    "Well":"qualitycontroltype"
}

rnaAD = {
    "id":"id",
    "Integrity":"integritynumber",
    "Range":"sizerange",
    "Size":"averagesizeinrange",
    "Conc":"concentration",
    "Molarity":"concentrationmolarinrange",
    "Well":"qualitycontroltype"
}

class QC_Dataset:

    def __init__(self, entity_data):

        self.bfabric_dataset = pd.DataFrame(
            entity_data['sample_data']
        )
        self.upload_dataset = ""
        self.plate_number = ""
        self.merged_dataset = ""
        self.instrument_type = ""
        self.TS_type = ""
        self.table_type = ""
        self.missing_wells_alert = []

    @property  
    def json(self):
        if hasattr(self, 'merged_dataset') and type(self.merged_dataset) == type(pd.DataFrame()): 
            return self.merged_dataset.to_json(date_format='iso', orient='split')
        else:
            return None
        
        
    @staticmethod
    def df_from_json(json):
        return pd.read_json(json, orient='split')
    

    def merged(self):

        csv_data = self.upload_dataset
        bfabric_data = self.bfabric_dataset

        if self.table_type == "ST" or self.table_type == "CRT":
            csv_data = csv_data[csv_data['Sample Description'] != "Ladder"]
            csv_data = csv_data[csv_data['Sample Description'] != "Electronic Ladder"]
            conc = ''

            for elt in list(csv_data.columns):
                if str(elt).startswith("Conc"):
                    conc = str(elt)
            for elt in list(csv_data.columns):
                if "mol" in str(elt).lower():
                    mol = str(elt)

            if conc == '':
                #TODO
                pass

        else:
            print(csv_data )
            print(bfabric_data)
        if self.table_type == "ST":

            tmp_df = pd.merge(bfabric_data, csv_data, how='inner', on=['Well'])

            # Identify rows with missing data in specific columns (RINe or Conc)
            missing_data_rows = tmp_df[tmp_df[['RINe', 'Conc. [pg/µl]']].isnull().any(axis=1)]

            if not missing_data_rows.empty:
                # Initialize missing wells alert
                self.missing_wells_alert = []

                # Iterate over rows with missing data
                for _, row in missing_data_rows.iterrows():
                    well = row['Well']
                    missing_columns = []
                    
                    # Check which specific columns are missing
                    if pd.isnull(row['RINe']):
                        missing_columns.append("Integrity")
                    if pd.isnull(row['Conc. [pg/µl]']):
                        missing_columns.append("Conc")

                    # TODO: Change procedure for checking missing data in other columns
                    # 1) iterate over ["RINe", "Conc. [pg/µl]", "Conc. [ng/µl]"]
                    
                    # Create alert message for the well
                    missing_info = ", ".join(missing_columns)  # Combine missing column names
                    self.missing_wells_alert.append(f"{well} is missing data in: {missing_info}")

                # Remove rows with missing data in RINe or Conc from tmp_df
                tmp_df = tmp_df.dropna(subset=['RINe', 'Conc. [pg/µl]'])

            if self.TS_type == "gDNA":
                df = pd.DataFrame({"Well":tmp_df['Well'],
                                  "id":tmp_df['ids'],
                                  "Integrity":tmp_df['DIN'],
                                  "Conc":tmp_df[conc]})

            elif self.TS_type == "HSD1k":
                df = pd.DataFrame({"Well":tmp_df['Well'],
                                  "id":tmp_df['ids'],
                                  "Conc":tmp_df[conc]/1000,
                                  "Range":["100 to 1000" for i in range(len(list(tmp_df['ids'])))]})

            elif self.TS_type == "D1k":
                df = pd.DataFrame({"Well":tmp_df['Well'],
                                  "id":tmp_df['ids'],
                                  "Conc":tmp_df[conc],
                                  "Range":["100 to 1000" for i in range(len(list(tmp_df['ids'])))]})

            elif self.TS_type == "D5k":
                df = pd.DataFrame({"Well":tmp_df['Well'],
                                  "id":tmp_df['ids'],
                                  "Conc":tmp_df[conc],
                                  "Range":["100 to 5000" for i in range(len(list(tmp_df['ids'])))]})

            elif self.TS_type == "HSD5k":
                df = pd.DataFrame({"Well":tmp_df['Well'],
                                  "id":tmp_df['ids'],
                                  "Conc":tmp_df[conc]/1000,
                                  "Range":["100 to 5000" for i in range(len(list(tmp_df['ids'])))]})

            elif self.TS_type == "RNA":
                df = pd.DataFrame({"Well":tmp_df['Well'],
                                  "id":tmp_df['ids'],
                                  "Conc":tmp_df[conc],
                                  "Integrity":tmp_df['RINe']})

            elif self.TS_type == "HSRNA":
                df = pd.DataFrame({"Well":tmp_df['Well'],
                                  "id":tmp_df['ids'],
                                  "Conc":tmp_df[conc]/1000,
                                  "Integrity":tmp_df['RINe']})
            else:
                #TODO
                pass

        elif self.table_type == "CRT":

            csv_data['Well'] = csv_data['WellId']
            csv_data['width'] = csv_data['To [bp]'] - csv_data['From [bp]']
            csv_data.drop_duplicates('Well')
            tmp_df = pd.merge(bfabric_data, csv_data, how='inner',on=['Well'])

            rnge = []
            frm = list(tmp_df['From [bp]'])
            to = list(tmp_df['To [bp]'])

            for i in range(len(frm)):
                rnge.append(str(frm[i]) + "bp to " + str(to[i]) + "bp")

            tmp_df['Range'] = rnge

            if self.TS_type == "gDNA":
                df = pd.DataFrame({"Well":tmp_df['Well'],
                                  "id":tmp_df['ids'],
                                  "Integrity":tmp_df['DIN'],
                                  "Conc":tmp_df[conc],
                                  "Range":tmp_df['Range']})

            elif self.TS_type == "HSD1k":
                df = pd.DataFrame({"Well":tmp_df['Well'],
                                  "id":tmp_df['ids'],
                                  "Conc":tmp_df[conc]/1000,
                                  "Range":tmp_df['Range'],
                                  "Size":tmp_df['Average Size [bp]']})

            elif self.TS_type == "D1k":
                df = pd.DataFrame({"Well":tmp_df['Well'],
                                  "id":tmp_df['ids'],
                                  "Conc":tmp_df[conc],
                                  "Range":tmp_df['Range'],
                                  "Size":tmp_df['Average Size [bp]']})

            elif self.TS_type == "D5k":
                df = pd.DataFrame({"Well":tmp_df['Well'],
                                  "id":tmp_df['ids'],
                                  "Conc":tmp_df[conc],
                                  "Range":tmp_df['Range'],
                                  "Size":tmp_df['Average Size [bp]']})

            elif self.TS_type == "HSD5k":
                df = pd.DataFrame({"Well":tmp_df['Well'],
                                  "id":tmp_df['ids'],
                                  "Conc":tmp_df[conc]/1000,
                                  "Range":tmp_df['Range'],
                                  "Size":tmp_df['Average Size [bp]']})

            elif self.TS_type == "RNA":
                df = pd.DataFrame({"Well":tmp_df['Well'],
                                  "id":tmp_df['ids'],
                                  "Conc":tmp_df[conc],
                                  "Integrity":tmp_df['RINe'],
                                  "Range":tmp_df['Range'],
                                  "Size":tmp_df['Average Size [bp]']})

            elif self.TS_type == "HSRNA":
                df = pd.DataFrame({"Well":tmp_df['Well'],
                                  "id":tmp_df['ids'],
                                  "Conc":tmp_df[conc]/1000,
                                  "Integrity":tmp_df['RINe'],
                                  "Range":tmp_df['Range'],
                                  "Size":tmp_df['Average Size [bp]']})

            try:
                if "HS" in self.TS_type:
                    df['Molarity'] = tmp_df[mol]/1000
                else:
                    df['Molarity'] = tmp_df[mol]
            except:
                #TODO
                pass

        elif self.table_type == "QbitUpload":

            if self.TS_type == "QDNA":
                print("Qubit DNA")
            elif self.TS_type == "QRNA":
                print("Qubit RNA")
            else:
                print("Unrecognized QC Type")

        elif self.table_type == "BioAnalyzerUpload":

            if self.TS_type == "BioA-DNA":
                print("BioAnalyzer DNA")
            elif self.TS_type == "BioA-RNA":
                print("BioAnalyzer RNA")
            else:
                print("Unrecognized QC Type")
            
        elif self.table_type == "BioRadUpload":
                
            if self.TS_type == "BioR-DNA":
                print("BioRad DNA")
            elif self.TS_type == "BioR-RNA":
                print("BioRad RNA")
            else:
                print("Unrecognized QC Type")

        elif self.table_type == "FemtoPulseUpload":
            
            if self.TS_type == "Femto-DNA":
                print("FemtoPulse DNA")
            elif self.TS_type == "Femto-RNA":
                print("FemtoPulse RNA")
            else:
                print("Unrecognized QC Type")

            
        elif self.table_type == "FAO":

            tmp_df = pd.merge(bfabric_data, csv_data, how='inner',on=['Well'])

            if self.TS_type == "FRAG_DNA":
                df = pd.DataFrame({"Well":tmp_df['Well'],
                                  "id":tmp_df['ids'],
                                  "Integrity":tmp_df['DQN'],
                                  "Conc":tmp_df["ng/uL"],
                                  "Molarity":tmp_df["nmole/L"],
                                  "Range":tmp_df['Range']})
                
            elif self.TS_type == "FRAG_RNA":
                df = pd.DataFrame({"Well":tmp_df['Well'],
                                  "id":tmp_df['ids'],
                                  "Integrity":tmp_df['RQN'],
                                  "Conc":tmp_df["Conc. (ng/ul)"],
                                  })
                


        else:
            print("CANNOT PROCEED -- "+str(self.table_type))

        for key in ["Conc", "Integrity", "Range", "Size", "Molarity"]:
            if key in df.columns:
                # TODO: deal with removing empty rows and alerting here. 
                pass

        self.merged_dataset = df

        return