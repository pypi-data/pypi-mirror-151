from nomnomdata.engine.components import Parameter, ParameterGroup, SharedConfig
from nomnomdata.engine.parameters import Code, Enum, Int, Nested, String

DOSpace = SharedConfig(
    shared_config_type_uuid="DOSPC-NND3C",
    description="DigitalOcean Space configuration parameters.",
    alias="DigitalOcean Space",
    categories=["DigitalOcean", "Spaces"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="space",
                display_name="Space Name",
                description="Specify the name of the Space.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="region",
                display_name="Region",
                description="Specify the region where the Space exists.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="path_prefix",
                display_name="Path Prefix",
                description="Optional. Specify a path that will be prepended to the path specified in a Task to form the full path where files will be stored within the Space.",
                required=False,
                type=String(),
            ),
            Parameter(
                name="temp_path",
                display_name="Temp Path",
                description="Optional. Specify a full path within the Space where temporary files can be written.",
                required=False,
                type=String(),
            ),
            name="do_space_parameters",
            display_name="Space Parameters",
            description="",
        ),
    ],
)


FirebaseToDatabase = SharedConfig(
    shared_config_type_uuid="FB2DB-NND3C",
    description="Firebase collection to a relational database table configuration parameters.",
    alias="Firebase to Relational Database",
    categories=[
        "Firebase",
        "Loader",
        "Relational Database",
    ],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="collection_name",
                display_name="Collection",
                description="Name of the collection in the Firebase app.",
                type=String(max=1024),
                required=True,
            ),
            Parameter(
                name="tracking_field",
                display_name="Tracking Field",
                description="Name of the field in the Collection to use for sorting and tracking documents processed.",
                required=False,
                type=String(),
            ),
            Parameter(
                name="tracking_field_type",
                display_name="Tracking Field Type",
                description="Select the data type of the Tracking Field.",
                required=False,
                type=Enum(choices=["NONE", "DATETIME", "STRING", "PUSHID"]),
                default="NONE",
            ),
            name="collection_parameters",
            display_name="Collection Parameters",
            description="Collection configuration information.",
        ),
        ParameterGroup(
            Parameter(
                name="load_pattern",
                display_name="Load Pattern",
                description="Select the pattern to use when loading the data.",
                type=Enum(choices=["INSERT"]),
                default="INSERT",
            ),
            Parameter(
                name="documentid_field",
                display_name="DocumentId Column",
                description="Map the DocumentId field to this column in the relational database.  Add a column with the same name to Column Parameters below.",
                type=String(),
                required=False,
            ),
            Parameter(
                name="date_processed_column",
                display_name="Date Processed Column",
                description="If specified, a date column representing when data was processed will be added to the relational database. Add a column with the same name to Column Parameters below.",
                type=String(),
                required=False,
            ),
            name="load_parameters",
            display_name="Load Parameters",
            description="Options for loading data into the relational database.",
        ),
        ParameterGroup(
            Parameter(
                name="column_parameters",
                display_name="Column Parameters",
                description="Details about each column within the relational database.",
                required=True,
                many=True,
                type=Nested(
                    Parameter(
                        name="column_name",
                        display_name="Column Name",
                        description="Specify the name of the column.",
                        type=String(max=128),
                        required=True,
                    ),
                    Parameter(
                        name="column_type",
                        display_name="Column Data Type",
                        description="Select the data type of the column. If type selected is not supported, the closest matching type will be used.",
                        type=Enum(
                            choices=[
                                "VARCHAR",
                                "INTEGER",
                                "BIGINT",
                                "DATETIME",
                                "DATE",
                                "TIME",
                                "TIMESTAMP",
                                "BOOLEAN",
                                "NUMERIC",
                                "FLOAT",
                                "BYTES",
                                "ARRAY",
                                "STRUCT",
                                "GEOGRAPHY",
                                # STRING
                            ]
                        ),
                        required=True,
                    ),
                    Parameter(
                        name="column_config",
                        display_name="Column Configuration",
                        description="Specify a configuration for the column. For example, VARCHAR could be (128), NUMERIC could be (12,2), ARRAY could be <STRING>, STRUCT could be <DATE, STRING>.",
                        type=String(),
                        required=False,
                    ),
                    Parameter(
                        name="json_path",
                        display_name="JSON Path",
                        description="Firebase field to map to the column. For example, ['store']['book']['title'] or store.book.title.",
                        type=String(),
                        required=False,
                    ),
                ),
            )
        ),
        ParameterGroup(
            Parameter(
                name="custom_parameter",
                display_name="Custom Parameters",
                description="Specify each parameter and value in quotes, separated by a colon.  Separate each pair with a comma and enclose all of the pairs in curly braces.",
                type=Code(),
                required=False,
            ),
            name="additional_parameters",
            display_name="Additional Parameters",
            description="Any additional parameters not described above.",
        ),
    ],
)

S3Bucket = SharedConfig(
    shared_config_type_uuid="S3BKT-NND3C",
    description="AWS S3 Bucket configuration parameters.",
    alias="S3 Bucket",
    categories=["Amazon", "AWS", "S3"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="bucket",
                display_name="Bucket Name",
                description="Specify the name of the S3 Bucket.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="region",
                display_name="Region",
                description="Optional. Specify the region where the Bucket exists.",
                type=String(),
                required=False,
            ),
            Parameter(
                name="path_prefix",
                display_name="Path Prefix",
                description="Optional. Specify a path that will be prepended to the path specified in a Task to form the full path where files will be stored within the Bucket.",
                required=False,
                type=String(),
            ),
            Parameter(
                name="temp_path",
                display_name="Temp Path",
                description="Optional. Specify a full path within the Bucket where temporary files can be written.",
                required=False,
                type=String(),
            ),
            name="s3_bucket_parameters",
            display_name="Bucket Parameters",
            description="",
        ),
    ],
)

S3FileToDatabase = SharedConfig(
    shared_config_type_uuid="S3BTK-DB3MD",
    alias="S3 to Relational Database Load Options",
    description="Information needed when loading data from files stored on S3 into a relational database.",
    categories=[
        "S3",
        "Loader",
        "Relational Database",
    ],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="bucket",
                display_name="Bucket",
                description="Specify the name of the S3 bucket that contains the files.",
                type=String(max=1024),
                required=True,
            ),
            Parameter(
                name="endpoint_url",
                display_name="Endpoint URL",
                description="For an S3 compatible bucket not hosted in AWS, specify the URL to reach it.",
                type=String(max=2048),
                required=False,
            ),
            Parameter(
                name="path",
                display_name="Path",
                description="Specify the path to the files within the S3 bucket.",
                type=String(max=2048),
                required=False,
            ),
            Parameter(
                name="s3_temp_space",
                display_name="Temporary File Storage Path",
                description="Specify the path within the S3 bucket where manifest files can be created.  If blank, nnd_tmp will be used.",
                type=String(max=2048),
                required=False,
            ),
            Parameter(
                name="region",
                display_name="Region",
                description="Optional. Specify the region where the Bucket exists.",
                type=String(),
                required=False,
            ),
            name="s3_parameters",
            display_name="S3 Parameters",
            description="Information about the S3 location where the files reside.",
        ),
        ParameterGroup(
            Parameter(
                name="load_pattern",
                display_name="Load Pattern",
                description="Select which pattern to use when loading the data from the files.",
                type=Enum(
                    choices=[
                        "INSERT",
                        "DELETE_ALL_INSERT_ALL",
                        "DELETE_ALL_INSERT_LAST",
                        "DELETE_INSERT",
                        "DELETE_INSERT_BATCH",
                        "DROP_AND_RECREATE",
                        "INSERT_IF_NOT_EXISTS",
                        "TRUNCATE_LOAD_ALL",
                        "TRUNCATE_LOAD_LAST",
                        "UPDATE_INSERT",
                        "UPDATE_INSERT_BATCH",
                    ]
                ),
                default="INSERT",
            ),
            Parameter(
                name="file_type",
                display_name="Data Format",
                description="Select the format of the data in the files.",
                type=Enum(choices=["JSON", "Delimited"]),
                default="JSON",
            ),
            Parameter(
                name="compression",
                display_name="Compression Format",
                description="Select the compression, if any, applied to the files.",
                type=Enum(choices=["None", "gzip", "zip", "bzip2"]),
                default="None",
            ),
            Parameter(
                name="delimiter",
                display_name="Delimiter",
                description="Specify the character used to separate data values in files with delimited data format.",
                type=String(max=2),
                required=False,
            ),
            Parameter(
                name="null_value",
                display_name="Null Value",
                description="Specify the characters used to represent a null value in files with delimited data format.",
                type=String(max=8),
                required=False,
            ),
            Parameter(
                name="escape_character",
                display_name="Escape Character",
                description="Specify the character used to represent an escaped value in files with delimited data format.",
                type=String(max=2),
                required=False,
            ),
            Parameter(
                name="header_rows",
                display_name="Header Rows",
                description="Specify the number of lines to skip before the first row of data in files with delimited data format.",
                type=Int(),
                required=False,
            ),
            name="load_parameters",
            display_name="Load Parameters",
            description="Options describing how the data from the files should be loaded.",
        ),
        ParameterGroup(
            Parameter(
                name="partition_key",
                display_name="Partition Key",
                description="Optional. Specify the name of the single column whose values will be used to partition each file's data.",
                type=String(max=1024),
                required=False,
            ),
            Parameter(
                name="sort_key",
                display_name="Sort Keys",
                description="Optional. Specify one or more column names, with commas between each name, whose values will be used to sort each file's data.",
                type=String(max=2048),
                required=False,
            ),
            Parameter(
                name="primary_key",
                display_name="Primary Key",
                description="Optional. Specify the name of the single column whose values will be used to uniquely identify each row within each file's data.",
                type=String(max=2048),
                required=False,
            ),
            Parameter(
                name="merge_key",
                display_name="Merge Keys",
                description="Optional. Specify one or more column names, with commas between each name, whose combined values will be used to identify rows of data that will be merged together.",
                type=String(max=2048),
                required=False,
            ),
            Parameter(
                name="upsert_sort_key",
                display_name="Upsert Sort Keys",
                description="Optional. Specify one or more column names, with commas between each name, whose combined values will be used to set the order priority of rows of data that will be merged together.",
                type=String(max=2048),
                required=False,
            ),
            Parameter(
                name="merge_type",
                display_name="Merge Strategy",
                description="If column names are specified in the Merge Keys field, then rows with matching merge key values will be combined according to the strategy selected.",
                type=Enum(choices=["DISTINCT", "LOAD_ALL"]),
                default="DISTINCT",
                required=False,
            ),
            name="key_parameters",
            display_name="Key Parameters",
            description="Columns used to partition, sort, identify and merge data.",
        ),
        Parameter(
            name="column_parameters",
            display_name="Column Parameters",
            description="Details about each column within the relational database.",
            required=True,
            many=True,
            type=Nested(
                Parameter(
                    name="column_name",
                    display_name="Column Name",
                    description="Specify the name of the column.",
                    type=String(max=128),
                    required=True,
                ),
                Parameter(
                    name="column_type",
                    display_name="Column Data Type",
                    description="Select the data type of the column. If type selected is not supported, the closest matching type will be used.",
                    type=Enum(
                        choices=[
                            "VARCHAR",
                            "INTEGER",
                            "BIGINT",
                            "DATETIME",
                            "DATE",
                            "TIME",
                            "TIMESTAMP",
                            "BOOLEAN",
                            "NUMERIC",
                            "FLOAT",
                            "BYTES",
                            "ARRAY",
                            "STRUCT",
                            "GEOGRAPHY",
                            # STRING
                        ]
                    ),
                    required=True,
                ),
                Parameter(
                    name="column_config",
                    display_name="Column Configuration",
                    description="Specify a configuration for the column. For example, VARCHAR could be (128), NUMERIC could be (12,2), ARRAY could be <STRING>, STRUCT could be <DATE, STRING>.",
                    type=String(),
                    required=False,
                ),
                Parameter(
                    name="json_path",
                    display_name="Field Mapping",
                    description="For JSON formatted files, specify the path to the field that matches this column. For example, ['store']['book']['title'] or store.book.title.",
                    type=String(),
                    required=False,
                ),
            ),
        ),
        ParameterGroup(
            Parameter(
                name="custom_parameter",
                display_name="Custom Parameters",
                description="Specify each parameter and value in quotes, separated by a colon.  Separate each pair with a comma and enclose all of the pairs in curly braces.",
                type=Code(),
                required=False,
            ),
            name="additional_parameters",
            display_name="Additional Parameters",
            description="",
        ),
    ],
)


VultrObjectStore = SharedConfig(
    shared_config_type_uuid="VULTR-OBJSR",
    description="Vultr Object Storage Bucket configuration parameters.",
    alias="Vultr Object Storage Bucket",
    categories=["Vultr", "Object Storage"],
    parameter_groups=[
        ParameterGroup(
            Parameter(
                name="bucket",
                display_name="Bucket Name",
                description="Specify the name of the Bucket.",
                type=String(),
                required=True,
            ),
            Parameter(
                name="region",
                display_name="Region",
                description="Specify the region where the Bucket exists.",
                type=Enum(choices=["ewr1"]),
                default="ewr1",
                required=True,
            ),
            Parameter(
                name="path_prefix",
                display_name="Path Prefix",
                description="Optional. Specify a path that will be prepended to the path specified in a Task to form the full path where files will be stored within the Bucket.",
                required=False,
                type=String(),
            ),
            Parameter(
                name="temp_path",
                display_name="Temp Path",
                description="Optional. Specify a full path within the Bucket where temporary files can be written.",
                required=False,
                type=String(),
            ),
            name="vultr_object_storage_parameters",
            display_name="Vultr Object Storage Parameters",
            description="",
        ),
    ],
)

KeyValue = SharedConfig(
    shared_config_type_uuid="GENRIC-KEYVAL",
    alias="Key and Value Pairs",
    description="One or more sets of key and value string pairs.",
    categories=[],
    parameter_groups=[
        Parameter(
            name="key_values",
            display_name="Pairs",
            description="",
            required=True,
            many=True,
            type=Nested(
                Parameter(
                    name="key",
                    display_name="Key",
                    description="Specify a key name.",
                    type=String(),
                    required=True,
                ),
                Parameter(
                    name="value",
                    display_name="Value",
                    description="Specify the value that corresponds to the key specified.",
                    type=String(),
                    required=True,
                ),
            ),
        ),
    ],
)
