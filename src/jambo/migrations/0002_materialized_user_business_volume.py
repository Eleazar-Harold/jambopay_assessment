# Generated by Django 4.1.13 on 2024-01-31 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jambo', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE MATERIALIZED VIEW user_business_volume AS
                SELECT
                concat(jambo_user.id, jambo_business.id, jambo_businesscategory.id, jambo_item.id) AS unique_id, 
                jambo_user.full_name as customer_name,
                jambo_user.phone_number as customer_phone_number,
                jambo_business.name as business_name,
                jambo_businesscategory.name as business_category,
                jambo_item.amount as amount,
                jambo_item.name as item_name,
                jambo_businessitem.year as year
                FROM jambo_businessitem
                INNER JOIN jambo_business ON jambo_business.id = jambo_businessitem.business_id
                INNER JOIN jambo_businesscategory ON jambo_business.category_id = jambo_businesscategory.id
                INNER JOIN jambo_item ON jambo_item.id = jambo_businessitem.item_id
                INNER JOIN jambo_user ON jambo_user.id = jambo_businessitem.user_id
                GROUP BY unique_id, customer_name, customer_phone_number, business_name, business_category, amount, item_name, year
                ORDER BY unique_id, year, business_category;
            """,
            "DROP VIEW user_business_volume;"
        ),
        migrations.RunSQL(
            """
            REFRESH MATERIALIZED VIEW user_business_volume;
            """,
            """
            REFRESH MATERIALIZED VIEW user_business_volume;
            """,
        ),
    ]
