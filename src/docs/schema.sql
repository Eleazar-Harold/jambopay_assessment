-- SQL dump generated using DBML (dbml-lang.org)
-- Database: PostgreSQL
-- Generated at: 2024-01-31T21:13:38.313Z

CREATE TABLE "User" (
  "id" bigserial,
  "password" char,
  "email" email,
  "full_name" varchar,
  "phone_number" bigint,
  "is_active" boolean,
  "customer" boolean,
  "admin" boolean,
  "timestamp" timestampz
);

CREATE TABLE "BusinessCategory" (
  "id" bigserial,
  "name" varchar,
  "timestamp" timestampz,
  "updated" timestampz
);

CREATE TABLE "Business" (
  "id" bigserial,
  "name" varchar,
  "active" boolean,
  "category_id" bigserial NOT NULL,
  "timestamp" timestampz,
  "updated" timestampz
);

CREATE TABLE "Item" (
  "id" bigserial,
  "name" varchar,
  "amount" float,
  "timestamp" timestampz,
  "updated" timestampz
);

CREATE TABLE "BusinessItem" (
  "id" bigserial,
  "user_id" bigserial NOT NULL,
  "business_id" bigserial NOT NULL,
  "item_id" bigserial NOT NULL,
  "year" bigint,
  "timestamp" timestampz,
  "updated" timestampz
);

CREATE INDEX ON "BusinessCategory" ("name");

CREATE INDEX ON "Business" ("name");

CREATE INDEX ON "Item" ("name");

CREATE INDEX ON "BusinessItem" ("year");

CREATE INDEX ON "BusinessItem" ("business_id");

CREATE INDEX ON "BusinessItem" ("item_id");

ALTER TABLE "Business" ADD FOREIGN KEY ("category_id") REFERENCES "BusinessCategory" ("id");

ALTER TABLE "BusinessItem" ADD FOREIGN KEY ("user_id") REFERENCES "User" ("id");

ALTER TABLE "BusinessItem" ADD FOREIGN KEY ("business_id") REFERENCES "Business" ("id");

ALTER TABLE "BusinessItem" ADD FOREIGN KEY ("item_id") REFERENCES "Item" ("id");
