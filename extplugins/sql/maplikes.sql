CREATE TABLE IF NOT EXISTS `maplikes` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `client_id` int(10) NOT NULL,
  `map` varchar(30) NOT NULL,
  `likes` tinyint(1) NOT NULL,
  `last_voted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `changes_left` INT(1) NOT NULL DEFAULT '3',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;