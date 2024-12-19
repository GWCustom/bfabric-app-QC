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

        alert_messages = {}

        relevant_columns = [col for col in ["Conc", "Integrity", "Range", "Size", "Molarity"] if col in df.columns]

        for key in relevant_columns:
            # Identify rows with missing data in the current column
            missing_data_rows = df[df[key].isnull()]

            if not missing_data_rows.empty:
                # Iterate over rows with missing data for the current column
                for _, row in missing_data_rows.iterrows():
                    well = row['Well'] if 'Well' in row else "Unknown Well"

                    # Append the current column to the alert message for this well
                    if well in alert_messages:
                        alert_messages[well].append(key)
                    else:
                        alert_messages[well] = [key]

        # Format and sort the alert messages alphabetically
        self.missing_wells_alert = sorted(
            [f"{well} is missing data in: {', '.join(columns)}" for well, columns in alert_messages.items()]
        )

        df = df.dropna(subset=relevant_columns, how='any')

        self.merged_dataset = df

        return