DELETE FROM movie_age_ratings;
DELETE FROM movie_genres;
DELETE FROM age_ratings;
DELETE FROM genres;

INSERT INTO genres (name) VALUES ('toiminta');
INSERT INTO genres (name) VALUES ('animaatio');
INSERT INTO genres (name) VALUES ('dokumentti');
INSERT INTO genres (name) VALUES ('draama');
INSERT INTO genres (name) VALUES ('kauhu');
INSERT INTO genres (name) VALUES ('komedia');
INSERT INTO genres (name) VALUES ('romanttinen');
INSERT INTO genres (name) VALUES ('scifi');
INSERT INTO genres (name) VALUES ('seikkailu');
INSERT INTO genres (name) VALUES ('trilleri');

INSERT INTO age_ratings (name) VALUES ('S');
INSERT INTO age_ratings (name) VALUES ('7');
INSERT INTO age_ratings (name) VALUES ('12');
INSERT INTO age_ratings (name) VALUES ('16');
INSERT INTO age_ratings (name) VALUES ('18');
