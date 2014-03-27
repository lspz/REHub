-- Count by suburb

SELECT
  sub.name,
  count(listing.id)
FROM rescrap_suburb sub
INNER JOIN rescrap_address addr on addr.suburb_id = sub.id
INNER JOIN rescrap_listing listing on listing.address_id = addr.id
GROUP BY 
  sub.id, sub.name
ORDER BY 
  count(listing.id) DESC
  
-- Count by address

SELECT
   addr.address,
  count(listing.id)
FROM rescrap_suburb sub
INNER JOIN rescrap_address addr on addr.suburb_id = sub.id
INNER JOIN rescrap_listing listing on listing.address_id = addr.id
GROUP BY 
  addr.id, addr.address
ORDER BY 
  count(listing.id) DESC
  
-- Batch history
SELECT
  batch.id,
  count(listing.id)
FROM rescrap_importbatch batch
INNER JOIN rescrap_listing listing on listing.batch_id = batch.id
GROUP BY 
  batch.id, batch.date
ORDER BY 
  batch.date DESC


-- Listing from latest import 
SELECT
  addr.*,
  suburb.*,
  lst.*
FROM rescrap_listing lst 
INNER JOIN rescrap_address addr on addr.id = lst.address_id
INNER JOIN rescrap_suburb suburb on suburb.id = addr.suburb_id
WHERE lst.batch_id = 
  (select batch.id 
   from rescrap_importbatch batch 
   ORDER BY batch.date 
   DESC LIMIT 1)
   
   
-- Address with multiple listing source 
SELECT 
  addr2.*
 FROM
 (
	SELECT
	  addr.id
	FROM rescrap_listing lst 
	INNER JOIN rescrap_address addr on addr.id = lst.address_id
	GROUP BY
	  addr.id
	HAVING 
	  count(distinct lst.source_id) >1
 ) addr1
 INNER JOIN rescrap_address addr2 on addr2.id = addr1.id