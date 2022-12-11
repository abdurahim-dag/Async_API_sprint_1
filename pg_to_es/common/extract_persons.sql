with persons as (
    select
        id,
        created,
        modified,
        full_name
    from {from_schema}.person
)
select
    json_build_object('id', g.id,
                      'full_name', coalesce(g.name, ''),
        )
    ) as "xyz"
from person p
where
    (p.modified > '{date_from}' or p.created > '{date_from}')
  and
    (pmodified <= '{date_to}' or p.created <= '{date_to}')
order by p.id
offset {offset};
