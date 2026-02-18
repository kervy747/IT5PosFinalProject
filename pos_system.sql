-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 18, 2026 at 01:08 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `phpmyadmin`
--
CREATE DATABASE IF NOT EXISTS `phpmyadmin` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;
USE `phpmyadmin`;

-- --------------------------------------------------------

--
-- Table structure for table `pma__bookmark`
--

CREATE TABLE `pma__bookmark` (
  `id` int(10) UNSIGNED NOT NULL,
  `dbase` varchar(255) NOT NULL DEFAULT '',
  `user` varchar(255) NOT NULL DEFAULT '',
  `label` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `query` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Bookmarks';

-- --------------------------------------------------------

--
-- Table structure for table `pma__central_columns`
--

CREATE TABLE `pma__central_columns` (
  `db_name` varchar(64) NOT NULL,
  `col_name` varchar(64) NOT NULL,
  `col_type` varchar(64) NOT NULL,
  `col_length` text DEFAULT NULL,
  `col_collation` varchar(64) NOT NULL,
  `col_isNull` tinyint(1) NOT NULL,
  `col_extra` varchar(255) DEFAULT '',
  `col_default` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Central list of columns';

-- --------------------------------------------------------

--
-- Table structure for table `pma__column_info`
--

CREATE TABLE `pma__column_info` (
  `id` int(5) UNSIGNED NOT NULL,
  `db_name` varchar(64) NOT NULL DEFAULT '',
  `table_name` varchar(64) NOT NULL DEFAULT '',
  `column_name` varchar(64) NOT NULL DEFAULT '',
  `comment` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `mimetype` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `transformation` varchar(255) NOT NULL DEFAULT '',
  `transformation_options` varchar(255) NOT NULL DEFAULT '',
  `input_transformation` varchar(255) NOT NULL DEFAULT '',
  `input_transformation_options` varchar(255) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Column information for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__designer_settings`
--

CREATE TABLE `pma__designer_settings` (
  `username` varchar(64) NOT NULL,
  `settings_data` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Settings related to Designer';

--
-- Dumping data for table `pma__designer_settings`
--

INSERT INTO `pma__designer_settings` (`username`, `settings_data`) VALUES
('root', '{\"relation_lines\":\"true\",\"snap_to_grid\":\"off\",\"angular_direct\":\"direct\"}');

-- --------------------------------------------------------

--
-- Table structure for table `pma__export_templates`
--

CREATE TABLE `pma__export_templates` (
  `id` int(5) UNSIGNED NOT NULL,
  `username` varchar(64) NOT NULL,
  `export_type` varchar(10) NOT NULL,
  `template_name` varchar(64) NOT NULL,
  `template_data` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Saved export templates';

--
-- Dumping data for table `pma__export_templates`
--

INSERT INTO `pma__export_templates` (`id`, `username`, `export_type`, `template_name`, `template_data`) VALUES
(1, 'root', 'table', 'T360db', '{\"quick_or_custom\":\"quick\",\"what\":\"sql\",\"allrows\":\"1\",\"aliases_new\":\"\",\"output_format\":\"sendit\",\"filename_template\":\"@TABLE@\",\"remember_template\":\"on\",\"charset\":\"utf-8\",\"compression\":\"none\",\"maxsize\":\"\",\"codegen_structure_or_data\":\"data\",\"codegen_format\":\"0\",\"csv_separator\":\",\",\"csv_enclosed\":\"\\\"\",\"csv_escaped\":\"\\\"\",\"csv_terminated\":\"AUTO\",\"csv_null\":\"NULL\",\"csv_columns\":\"something\",\"csv_structure_or_data\":\"data\",\"excel_null\":\"NULL\",\"excel_columns\":\"something\",\"excel_edition\":\"win\",\"excel_structure_or_data\":\"data\",\"json_structure_or_data\":\"data\",\"json_unicode\":\"something\",\"latex_caption\":\"something\",\"latex_structure_or_data\":\"structure_and_data\",\"latex_structure_caption\":\"Structure of table @TABLE@\",\"latex_structure_continued_caption\":\"Structure of table @TABLE@ (continued)\",\"latex_structure_label\":\"tab:@TABLE@-structure\",\"latex_relation\":\"something\",\"latex_comments\":\"something\",\"latex_mime\":\"something\",\"latex_columns\":\"something\",\"latex_data_caption\":\"Content of table @TABLE@\",\"latex_data_continued_caption\":\"Content of table @TABLE@ (continued)\",\"latex_data_label\":\"tab:@TABLE@-data\",\"latex_null\":\"\\\\textit{NULL}\",\"mediawiki_structure_or_data\":\"data\",\"mediawiki_caption\":\"something\",\"mediawiki_headers\":\"something\",\"htmlword_structure_or_data\":\"structure_and_data\",\"htmlword_null\":\"NULL\",\"ods_null\":\"NULL\",\"ods_structure_or_data\":\"data\",\"odt_structure_or_data\":\"structure_and_data\",\"odt_relation\":\"something\",\"odt_comments\":\"something\",\"odt_mime\":\"something\",\"odt_columns\":\"something\",\"odt_null\":\"NULL\",\"pdf_report_title\":\"\",\"pdf_structure_or_data\":\"data\",\"phparray_structure_or_data\":\"data\",\"sql_include_comments\":\"something\",\"sql_header_comment\":\"\",\"sql_use_transaction\":\"something\",\"sql_compatibility\":\"NONE\",\"sql_structure_or_data\":\"structure_and_data\",\"sql_create_table\":\"something\",\"sql_auto_increment\":\"something\",\"sql_create_view\":\"something\",\"sql_create_trigger\":\"something\",\"sql_backquotes\":\"something\",\"sql_type\":\"INSERT\",\"sql_insert_syntax\":\"both\",\"sql_max_query_size\":\"50000\",\"sql_hex_for_binary\":\"something\",\"sql_utc_time\":\"something\",\"texytext_structure_or_data\":\"structure_and_data\",\"texytext_null\":\"NULL\",\"xml_structure_or_data\":\"data\",\"xml_export_events\":\"something\",\"xml_export_functions\":\"something\",\"xml_export_procedures\":\"something\",\"xml_export_tables\":\"something\",\"xml_export_triggers\":\"something\",\"xml_export_views\":\"something\",\"xml_export_contents\":\"something\",\"yaml_structure_or_data\":\"data\",\"\":null,\"lock_tables\":null,\"csv_removeCRLF\":null,\"excel_removeCRLF\":null,\"json_pretty_print\":null,\"htmlword_columns\":null,\"ods_columns\":null,\"sql_dates\":null,\"sql_relation\":null,\"sql_mime\":null,\"sql_disable_fk\":null,\"sql_views_as_tables\":null,\"sql_metadata\":null,\"sql_drop_table\":null,\"sql_if_not_exists\":null,\"sql_simple_view_export\":null,\"sql_view_current_user\":null,\"sql_or_replace_view\":null,\"sql_procedure_function\":null,\"sql_truncate\":null,\"sql_delayed\":null,\"sql_ignore\":null,\"texytext_columns\":null}');

-- --------------------------------------------------------

--
-- Table structure for table `pma__favorite`
--

CREATE TABLE `pma__favorite` (
  `username` varchar(64) NOT NULL,
  `tables` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Favorite tables';

-- --------------------------------------------------------

--
-- Table structure for table `pma__history`
--

CREATE TABLE `pma__history` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `username` varchar(64) NOT NULL DEFAULT '',
  `db` varchar(64) NOT NULL DEFAULT '',
  `table` varchar(64) NOT NULL DEFAULT '',
  `timevalue` timestamp NOT NULL DEFAULT current_timestamp(),
  `sqlquery` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='SQL history for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__navigationhiding`
--

CREATE TABLE `pma__navigationhiding` (
  `username` varchar(64) NOT NULL,
  `item_name` varchar(64) NOT NULL,
  `item_type` varchar(64) NOT NULL,
  `db_name` varchar(64) NOT NULL,
  `table_name` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Hidden items of navigation tree';

-- --------------------------------------------------------

--
-- Table structure for table `pma__pdf_pages`
--

CREATE TABLE `pma__pdf_pages` (
  `db_name` varchar(64) NOT NULL DEFAULT '',
  `page_nr` int(10) UNSIGNED NOT NULL,
  `page_descr` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='PDF relation pages for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__recent`
--

CREATE TABLE `pma__recent` (
  `username` varchar(64) NOT NULL,
  `tables` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Recently accessed tables';

--
-- Dumping data for table `pma__recent`
--

INSERT INTO `pma__recent` (`username`, `tables`) VALUES
('root', '[{\"db\":\"pos_system\",\"table\":\"products\"},{\"db\":\"pos_system\",\"table\":\"system_settings\"},{\"db\":\"pos_system\",\"table\":\"transaction_items\"},{\"db\":\"pos_system\",\"table\":\"transactions\"},{\"db\":\"pos_system\",\"table\":\"users\"}]');

-- --------------------------------------------------------

--
-- Table structure for table `pma__relation`
--

CREATE TABLE `pma__relation` (
  `master_db` varchar(64) NOT NULL DEFAULT '',
  `master_table` varchar(64) NOT NULL DEFAULT '',
  `master_field` varchar(64) NOT NULL DEFAULT '',
  `foreign_db` varchar(64) NOT NULL DEFAULT '',
  `foreign_table` varchar(64) NOT NULL DEFAULT '',
  `foreign_field` varchar(64) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Relation table';

-- --------------------------------------------------------

--
-- Table structure for table `pma__savedsearches`
--

CREATE TABLE `pma__savedsearches` (
  `id` int(5) UNSIGNED NOT NULL,
  `username` varchar(64) NOT NULL DEFAULT '',
  `db_name` varchar(64) NOT NULL DEFAULT '',
  `search_name` varchar(64) NOT NULL DEFAULT '',
  `search_data` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Saved searches';

-- --------------------------------------------------------

--
-- Table structure for table `pma__table_coords`
--

CREATE TABLE `pma__table_coords` (
  `db_name` varchar(64) NOT NULL DEFAULT '',
  `table_name` varchar(64) NOT NULL DEFAULT '',
  `pdf_page_number` int(11) NOT NULL DEFAULT 0,
  `x` float UNSIGNED NOT NULL DEFAULT 0,
  `y` float UNSIGNED NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Table coordinates for phpMyAdmin PDF output';

-- --------------------------------------------------------

--
-- Table structure for table `pma__table_info`
--

CREATE TABLE `pma__table_info` (
  `db_name` varchar(64) NOT NULL DEFAULT '',
  `table_name` varchar(64) NOT NULL DEFAULT '',
  `display_field` varchar(64) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Table information for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__table_uiprefs`
--

CREATE TABLE `pma__table_uiprefs` (
  `username` varchar(64) NOT NULL,
  `db_name` varchar(64) NOT NULL,
  `table_name` varchar(64) NOT NULL,
  `prefs` text NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Tables'' UI preferences';

-- --------------------------------------------------------

--
-- Table structure for table `pma__tracking`
--

CREATE TABLE `pma__tracking` (
  `db_name` varchar(64) NOT NULL,
  `table_name` varchar(64) NOT NULL,
  `version` int(10) UNSIGNED NOT NULL,
  `date_created` datetime NOT NULL,
  `date_updated` datetime NOT NULL,
  `schema_snapshot` text NOT NULL,
  `schema_sql` text DEFAULT NULL,
  `data_sql` longtext DEFAULT NULL,
  `tracking` set('UPDATE','REPLACE','INSERT','DELETE','TRUNCATE','CREATE DATABASE','ALTER DATABASE','DROP DATABASE','CREATE TABLE','ALTER TABLE','RENAME TABLE','DROP TABLE','CREATE INDEX','DROP INDEX','CREATE VIEW','ALTER VIEW','DROP VIEW') DEFAULT NULL,
  `tracking_active` int(1) UNSIGNED NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Database changes tracking for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__userconfig`
--

CREATE TABLE `pma__userconfig` (
  `username` varchar(64) NOT NULL,
  `timevalue` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `config_data` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='User preferences storage for phpMyAdmin';

--
-- Dumping data for table `pma__userconfig`
--

INSERT INTO `pma__userconfig` (`username`, `timevalue`, `config_data`) VALUES
('root', '2026-02-05 09:24:56', '{\"Console\\/Mode\":\"show\"}');

-- --------------------------------------------------------

--
-- Table structure for table `pma__usergroups`
--

CREATE TABLE `pma__usergroups` (
  `usergroup` varchar(64) NOT NULL,
  `tab` varchar(64) NOT NULL,
  `allowed` enum('Y','N') NOT NULL DEFAULT 'N'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='User groups with configured menu items';

-- --------------------------------------------------------

--
-- Table structure for table `pma__users`
--

CREATE TABLE `pma__users` (
  `username` varchar(64) NOT NULL,
  `usergroup` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Users and their assignments to user groups';

--
-- Indexes for dumped tables
--

--
-- Indexes for table `pma__bookmark`
--
ALTER TABLE `pma__bookmark`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pma__central_columns`
--
ALTER TABLE `pma__central_columns`
  ADD PRIMARY KEY (`db_name`,`col_name`);

--
-- Indexes for table `pma__column_info`
--
ALTER TABLE `pma__column_info`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `db_name` (`db_name`,`table_name`,`column_name`);

--
-- Indexes for table `pma__designer_settings`
--
ALTER TABLE `pma__designer_settings`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pma__export_templates`
--
ALTER TABLE `pma__export_templates`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `u_user_type_template` (`username`,`export_type`,`template_name`);

--
-- Indexes for table `pma__favorite`
--
ALTER TABLE `pma__favorite`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pma__history`
--
ALTER TABLE `pma__history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username` (`username`,`db`,`table`,`timevalue`);

--
-- Indexes for table `pma__navigationhiding`
--
ALTER TABLE `pma__navigationhiding`
  ADD PRIMARY KEY (`username`,`item_name`,`item_type`,`db_name`,`table_name`);

--
-- Indexes for table `pma__pdf_pages`
--
ALTER TABLE `pma__pdf_pages`
  ADD PRIMARY KEY (`page_nr`),
  ADD KEY `db_name` (`db_name`);

--
-- Indexes for table `pma__recent`
--
ALTER TABLE `pma__recent`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pma__relation`
--
ALTER TABLE `pma__relation`
  ADD PRIMARY KEY (`master_db`,`master_table`,`master_field`),
  ADD KEY `foreign_field` (`foreign_db`,`foreign_table`);

--
-- Indexes for table `pma__savedsearches`
--
ALTER TABLE `pma__savedsearches`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `u_savedsearches_username_dbname` (`username`,`db_name`,`search_name`);

--
-- Indexes for table `pma__table_coords`
--
ALTER TABLE `pma__table_coords`
  ADD PRIMARY KEY (`db_name`,`table_name`,`pdf_page_number`);

--
-- Indexes for table `pma__table_info`
--
ALTER TABLE `pma__table_info`
  ADD PRIMARY KEY (`db_name`,`table_name`);

--
-- Indexes for table `pma__table_uiprefs`
--
ALTER TABLE `pma__table_uiprefs`
  ADD PRIMARY KEY (`username`,`db_name`,`table_name`);

--
-- Indexes for table `pma__tracking`
--
ALTER TABLE `pma__tracking`
  ADD PRIMARY KEY (`db_name`,`table_name`,`version`);

--
-- Indexes for table `pma__userconfig`
--
ALTER TABLE `pma__userconfig`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pma__usergroups`
--
ALTER TABLE `pma__usergroups`
  ADD PRIMARY KEY (`usergroup`,`tab`,`allowed`);

--
-- Indexes for table `pma__users`
--
ALTER TABLE `pma__users`
  ADD PRIMARY KEY (`username`,`usergroup`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `pma__bookmark`
--
ALTER TABLE `pma__bookmark`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pma__column_info`
--
ALTER TABLE `pma__column_info`
  MODIFY `id` int(5) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pma__export_templates`
--
ALTER TABLE `pma__export_templates`
  MODIFY `id` int(5) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `pma__history`
--
ALTER TABLE `pma__history`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pma__pdf_pages`
--
ALTER TABLE `pma__pdf_pages`
  MODIFY `page_nr` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pma__savedsearches`
--
ALTER TABLE `pma__savedsearches`
  MODIFY `id` int(5) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- Database: `pos_system`
--
CREATE DATABASE IF NOT EXISTS `pos_system` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `pos_system`;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` varchar(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL CHECK (`price` >= 0),
  `stock` int(11) NOT NULL CHECK (`stock` >= 0),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `name`, `price`, `stock`, `created_at`, `updated_at`) VALUES
('PR00001', 'Lucky 65 Keyboard', 3000.00, 74, '2026-01-25 03:57:44', '2026-02-12 05:17:43'),
('PR00002', 'Intel Core i9-14900K CPU', 32999.00, 14, '2025-12-17 14:23:56', '2026-02-12 05:39:46'),
('PR00003', 'AMD Ryzen 9 7950X CPU', 30999.00, 4, '2025-12-17 14:23:56', '2025-12-18 03:24:44'),
('PR00004', 'AMD RX 7900 XTX GPU', 50999.00, 5, '2025-12-17 14:23:56', '2025-12-18 03:19:09'),
('PR00005', 'Corsair Vengeance 32GB DDR5 RAM', 7299.00, 9, '2025-12-17 14:23:56', '2025-12-18 18:08:06'),
('PR00006', 'G.Skill Trident Z5 64GB DDR5 RAM', 14099.00, 15, '2025-12-17 14:23:56', '2026-02-10 13:08:45'),
('PR00007', 'ASUS ROG Strix Z790 Motherboard', 25399.00, 4, '2025-12-17 14:23:56', '2026-02-10 13:08:45'),
('PR00008', 'MSI MAG B650 Motherboard', 11299.00, 10, '2025-12-17 14:23:56', '2025-12-18 18:07:44'),
('PR00009', 'Corsair RM1000e 1000W PSU', 10199.00, 7, '2025-12-17 14:23:56', '2026-02-10 13:08:45'),
('PR00010', 'EVGA SuperNOVA 850W PSU', 7349.00, 11, '2025-12-17 14:23:56', '2025-12-18 22:25:02'),
('PR00011', 'NZXT H7 Flow PC Case', 7349.00, 3, '2025-12-17 14:23:56', '2025-12-18 22:47:43'),
('PR00012', 'Lian Li O11 Dynamic PC Case', 9049.00, 3, '2025-12-17 14:23:56', '2026-02-10 13:08:45'),
('PR00013', 'MSi MAG A50', 1499.00, 22, '2025-12-17 14:23:56', '2025-12-18 22:47:43');

-- --------------------------------------------------------

--
-- Table structure for table `system_settings`
--

CREATE TABLE `system_settings` (
  `setting_key` varchar(50) NOT NULL,
  `setting_value` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `system_settings`
--

INSERT INTO `system_settings` (`setting_key`, `setting_value`) VALUES
('next_order_number', '56'),
('next_product_number', '16');

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `order_id` varchar(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `staff_name` varchar(50) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL CHECK (`total_amount` >= 0),
  `date` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`id`, `order_id`, `user_id`, `staff_name`, `total_amount`, `date`, `created_at`) VALUES
(2, 'OR0002', 7, 'John', 31046.00, '2025-12-16 04:55:00', '2025-12-17 14:23:56'),
(17, 'OR0005', 7, 'John', 41594.00, '12-19-2025 02:25 PM', '2025-12-18 22:25:02'),
(21, 'OR0009', 7, 'John', 81997.00, '11-08-2025 11:00 AM', '2025-11-07 19:00:00'),
(25, 'OR0013', 7, 'John', 50999.00, '11-17-2025 04:30 PM', '2025-11-17 00:30:00'),
(29, 'OR0017', 7, 'John', 17548.00, '11-27-2025 03:25 PM', '2025-11-26 23:25:00'),
(33, 'OR0021', 7, 'John', 93497.00, '12-06-2025 11:45 AM', '2025-12-05 19:45:00'),
(37, 'OR0025', 7, 'John', 25497.00, '12-13-2025 10:10 AM', '2025-12-12 18:10:00'),
(41, 'OR0029', 7, 'John', 32999.00, '12-23-2025 10:05 AM', '2025-12-22 18:05:00'),
(45, 'OR0033', 7, 'John', 30598.00, '01-06-2026 11:15 AM', '2026-01-05 19:15:00'),
(49, 'OR0037', 7, 'John', 24497.00, '01-16-2026 03:20 PM', '2026-01-15 23:20:00'),
(53, 'OR0041', 7, 'John', 65997.00, '01-27-2026 01:30 PM', '2026-01-26 21:30:00'),
(56, 'OR0043', 8, 'Maria', 58398.00, '02-01-2026 10:30 AM', '2026-01-31 18:30:00'),
(57, 'OR0044', 7, 'John', 76398.00, '02-03-2026 02:15 PM', '2026-02-02 22:15:00'),
(58, 'OR0045', 9, 'Alan', 14598.00, '02-05-2026 11:20 AM', '2026-02-04 19:20:00'),
(59, 'OR0046', 8, 'Maria', 50999.00, '02-07-2026 09:45 AM', '2026-02-06 17:45:00'),
(60, 'OR0047', 7, 'John', 28198.00, '02-10-2026 01:30 PM', '2026-02-09 21:30:00'),
(61, 'OR0048', 9, 'Alan', 42298.00, '02-12-2026 03:50 PM', '2026-02-11 23:50:00'),
(62, 'OR0049', 8, 'Maria', 20398.00, '02-15-2026 10:10 AM', '2026-02-14 18:10:00'),
(63, 'OR0050', 7, 'John', 24497.00, '02-18-2026 02:25 PM', '2026-02-17 22:25:00'),
(64, 'OR0051', 9, 'Alan', 9000.00, '02-21-2026 11:40 AM', '2026-02-20 19:40:00'),
(65, 'OR0052', 8, 'Maria', 61998.00, '02-25-2026 04:15 PM', '2026-02-25 00:15:00'),
(66, 'OR0053', 7, 'John', 70746.00, '02-10-2026 09:08 PM', '2026-02-10 13:08:45'),
(67, 'OR0054', 7, 'John', 101997.00, '02-12-2026 01:17 PM', '2026-02-12 05:17:43'),
(68, 'OR0055', 7, 'John', 98997.00, '02-12-2026 01:39 PM', '2026-02-12 05:39:46');

-- --------------------------------------------------------

--
-- Table structure for table `transaction_items`
--

CREATE TABLE `transaction_items` (
  `id` int(11) NOT NULL,
  `transaction_id` int(11) NOT NULL,
  `product_id` varchar(20) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `quantity` int(11) NOT NULL CHECK (`quantity` > 0),
  `price` decimal(10,2) NOT NULL CHECK (`price` >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transaction_items`
--

INSERT INTO `transaction_items` (`id`, `transaction_id`, `product_id`, `product_name`, `quantity`, `price`) VALUES
(3, 2, 'PR00005', 'Corsair Vengeance 32GB DDR5 RAM', 1, 7299.00),
(4, 2, 'PR00012', 'Lian Li O11 Dynamic PC Case', 1, 9049.00),
(5, 2, 'PR00010', 'EVGA SuperNOVA 850W PSU', 2, 7349.00),
(43, 17, 'PR00001', 'Lucky 65 Keyboard', 1, 3000.00),
(44, 17, 'PR00009', 'Corsair RM1000e 1000W PSU', 1, 10199.00),
(45, 17, 'PR00011', 'NZXT H7 Flow PC Case', 1, 7349.00),
(46, 17, 'PR00010', 'EVGA SuperNOVA 850W PSU', 3, 7349.00),
(47, 17, 'PR00013', 'MSi MAG A50', 1, 1499.00),
(56, 21, 'PR00003', 'AMD Ryzen 9 7950X CPU', 1, 30999.00),
(57, 21, 'PR00004', 'AMD RX 7900 XTX GPU', 1, 50999.00),
(65, 25, 'PR00004', 'AMD RX 7900 XTX GPU', 1, 50999.00),
(71, 29, 'PR00009', 'Corsair RM1000e 1000W PSU', 1, 10199.00),
(72, 29, 'PR00011', 'NZXT H7 Flow PC Case', 1, 7349.00),
(77, 33, 'PR00003', 'AMD Ryzen 9 7950X CPU', 2, 30999.00),
(78, 33, 'PR00003', 'AMD Ryzen 9 7950X CPU', 1, 30999.00),
(83, 37, 'PR00012', 'Lian Li O11 Dynamic PC Case', 2, 9049.00),
(84, 37, 'PR00005', 'Corsair Vengeance 32GB DDR5 RAM', 1, 7299.00),
(91, 41, 'PR00002', 'Intel Core i9-14900K CPU', 1, 32999.00),
(98, 45, 'PR00006', 'G.Skill Trident Z5 64GB DDR5 RAM', 1, 14099.00),
(99, 45, 'PR00005', 'Corsair Vengeance 32GB DDR5 RAM', 1, 7299.00),
(100, 45, 'PR00012', 'Lian Li O11 Dynamic PC Case', 1, 9049.00),
(108, 49, 'PR00009', 'Corsair RM1000e 1000W PSU', 1, 10199.00),
(109, 49, 'PR00006', 'G.Skill Trident Z5 64GB DDR5 RAM', 1, 14099.00),
(114, 53, 'PR00002', 'Intel Core i9-14900K CPU', 1, 32999.00),
(115, 53, 'PR00003', 'AMD Ryzen 9 7950X CPU', 1, 30999.00),
(116, 53, 'PR00013', 'MSi MAG A50', 2, 1499.00),
(119, 56, 'PR00002', 'Intel Core i9-14900K CPU', 1, 32999.00),
(120, 56, 'PR00007', 'ASUS ROG Strix Z790 Motherboard', 1, 25399.00),
(121, 57, 'PR00007', 'ASUS ROG Strix Z790 Motherboard', 1, 25399.00),
(122, 57, 'PR00004', 'AMD RX 7900 XTX GPU', 1, 50999.00),
(123, 58, 'PR00005', 'Corsair Vengeance 32GB DDR5 RAM', 2, 7299.00),
(124, 59, 'PR00004', 'AMD RX 7900 XTX GPU', 1, 50999.00),
(125, 60, 'PR00006', 'G.Skill Trident Z5 64GB DDR5 RAM', 2, 14099.00),
(126, 61, 'PR00008', 'MSI MAG B650 Motherboard', 1, 11299.00),
(127, 61, 'PR00003', 'AMD Ryzen 9 7950X CPU', 1, 30999.00),
(128, 62, 'PR00012', 'Lian Li O11 Dynamic PC Case', 1, 9049.00),
(129, 62, 'PR00008', 'MSI MAG B650 Motherboard', 1, 11299.00),
(130, 63, 'PR00009', 'Corsair RM1000e 1000W PSU', 1, 10199.00),
(131, 63, 'PR00006', 'G.Skill Trident Z5 64GB DDR5 RAM', 1, 14099.00),
(132, 64, 'PR00001', 'Lucky 65 Keyboard', 3, 3000.00),
(133, 65, 'PR00003', 'AMD Ryzen 9 7950X CPU', 2, 30999.00),
(134, 66, 'PR00007', 'ASUS ROG Strix Z790 Motherboard', 1, 25399.00),
(135, 66, 'PR00009', 'Corsair RM1000e 1000W PSU', 1, 10199.00),
(136, 66, 'PR00006', 'G.Skill Trident Z5 64GB DDR5 RAM', 1, 14099.00),
(137, 66, 'PR00012', 'Lian Li O11 Dynamic PC Case', 1, 9049.00),
(138, 66, 'PR00001', 'Lucky 65 Keyboard', 4, 3000.00),
(139, 67, 'PR00001', 'Lucky 65 Keyboard', 1, 3000.00),
(140, 67, 'PR00002', 'Intel Core i9-14900K CPU', 3, 32999.00),
(141, 68, 'PR00002', 'Intel Core i9-14900K CPU', 3, 32999.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','staff') NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `active` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`, `created_at`, `active`) VALUES
(1, 'admin', '$2b$12$L/Rwx1gcVtm.hMiVFvQUxeDQtJLaNbQFgpMQRERYK2CpvMRZvyG5a', 'admin', '2025-12-17 14:23:56', 1),
(2, 'Kervy', '$2b$12$ekT64e8ozcnOKialWlg3ZOL.6ssUE6lD4HiOv.hA6CbWEXC2bZzMy', 'admin', '2025-12-17 14:23:56', 1),
(7, 'John', '$2b$12$0pgdEe9rZxFqpJDa7ocoI.JE4.GtTHlI.ibYDF.RDTpWhiXnqfns2', 'staff', '2026-01-14 17:24:09', 1),
(8, 'Maria', '$2b$12$AslqP8m3j10dwrGQZrX/B.aAs2FPEYui.EhjBsnjbEGBbSNesAs6S', 'staff', '2026-02-03 01:06:26', 1),
(9, 'Alan', '$2b$12$/RG0xr.iMw/JQQurdA7FbOJB1.U24S48AxTly3tdoN6aVoDbT4mOi', 'staff', '2026-02-03 01:06:38', 1),
(10, 'Dany', '$2b$12$x.1NzLhhrM14lAO5Tu8ame2tfTTjhKydDYP4WAqMiz2w8dO0HfHYC', 'staff', '2026-02-05 09:40:26', 1),
(11, 'Alexa', '$2b$12$0qiEN8MdlNAH/RyJe/Cx5ekvN5X4OL2WyzYFXeAz0ICBEAnfKJg0m', 'staff', '2026-02-08 03:49:27', 1),
(12, 'testuser', '$2b$12$ya4uKAbamyA5h0qkAm1WIuA3DCJ35t97cFIRaqzeAzDKN1h2Svmi6', 'staff', '2026-02-10 14:29:15', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `system_settings`
--
ALTER TABLE `system_settings`
  ADD PRIMARY KEY (`setting_key`);

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `order_id` (`order_id`),
  ADD KEY `idx_order_id` (`order_id`),
  ADD KEY `idx_user_id` (`user_id`),
  ADD KEY `idx_staff_name` (`staff_name`);

--
-- Indexes for table `transaction_items`
--
ALTER TABLE `transaction_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_transaction_id` (`transaction_id`),
  ADD KEY `idx_product_id` (`product_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT for table `transaction_items`
--
ALTER TABLE `transaction_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=142;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `fk_transactions_staff_name` FOREIGN KEY (`staff_name`) REFERENCES `users` (`username`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_transactions_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `transaction_items`
--
ALTER TABLE `transaction_items`
  ADD CONSTRAINT `fk_transaction_items_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_transaction_items_transaction` FOREIGN KEY (`transaction_id`) REFERENCES `transactions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
--
-- Database: `test`
--
CREATE DATABASE IF NOT EXISTS `test` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `test`;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
