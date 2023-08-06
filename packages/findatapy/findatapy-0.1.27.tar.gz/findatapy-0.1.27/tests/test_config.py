## test function
if __name__ == "__main__":
    logger = LoggerManager().getLogger(__name__)

    data_constants = DataConstants(
        override_fields={"use_cache_compression": False})

    print(data_constants.use_cache_compression)

    cm = ConfigManager().get_instance()

    categories = cm.get_categories_from_fields()

    logger.info("Categories from fields list")
    print(categories)

    categories = cm.get_categories_from_tickers()

    logger.info("Categories from tickers list")
    print(categories)

    filter = "events"

    categories_filtered = cm.get_categories_from_tickers_selective_filter(
        filter)
    logger.info("Categories from tickers list, filtered by events")
    print(categories_filtered)

    logger.info("For each category, print all tickers and fields")

    for sing in categories:
        split_sing = sing.split(".")
        category = split_sing[0]
        data_source = split_sing[1]
        freq = split_sing[2]
        cut = split_sing[3]

        logger.info("tickers for " + sing)
        tickers = cm.get_tickers_list_for_category(category, data_source, freq,
                                                   cut)

        print(tickers)

        logger.info("fields for " + sing)
        fields = cm.get_fields_list_for_category(category, data_source, freq,
                                                 cut)

        print(fields)

    # test the various converter mechanisms
    output = cm.convert_library_to_vendor_ticker(category="fx",
                                                 data_source="bloomberg",
                                                 freq="daily", cut="TOK",
                                                 ticker="USDJPY")

    print(output)

    output = cm.convert_vendor_to_library_ticker(
        data_source="bloomberg", vendor_tickers="EURUSD CMPT Curncy")

    print(output)

    output = cm.convert_vendor_to_library_field(
        data_source="bloomberg", vendor_fields="PX_LAST")

    print(output)

    output = cm.convert_library_to_vendor_field(
        data_source="bloomberg", vendor_fields="close")

    print(output)

    print(DataConstants().use_cache_compression)
