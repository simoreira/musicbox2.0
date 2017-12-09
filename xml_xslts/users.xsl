<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:user="http://www.users.com/users#" xmlns:foaf="http://xmlns.com/foaf/spec/">

  <xsl:template match="/">
    <rdf:RDF>
      <rdf:Description rdf:about="http://www.users.com/users">
        <xsl:apply-templates/>
      </rdf:Description>
    </rdf:RDF>
  </xsl:template>

  <xsl:template match="user">
    <xsl:variable name="name"><xsl:value-of select="name"/></xsl:variable>
    <user:user>
      <rdf:Description rdf:about="http://www.users.com/users/{$name}">
        <foaf:name><xsl:value-of select="name"/></foaf:name>
        <user:email><xsl:value-of select="email"/></user:email>
        <user:password><xsl:value-of select="password"/></user:password>

        <xsl:for-each select="starred">
          <user:starred>
            <rdf:Description rdf:about="http://www.users.com/users/{$name}/starred">
              <xsl:for-each select="fav[@type='artist']">
                <user:favArt>
                  <rdf:Description rdf:about="http://www.users.com/users/{$name}/starred/{.}">
                    <foaf:favArt><xsl:value-of select="."/></foaf:favArt>
                  </rdf:Description>
                </user:favArt>
              </xsl:for-each>
              <xsl:for-each select="fav[@type='album']">
                <user:favAlb>
                  <rdf:Description rdf:about="http://www.users.com/users/{$name}/starred/{.}">
                    <foaf:favAlb><xsl:value-of select="."/></foaf:favAlb>
                  </rdf:Description>
                </user:favAlb>
              </xsl:for-each>
            </rdf:Description>
          </user:starred>
        </xsl:for-each>

      </rdf:Description>
    </user:user>
  </xsl:template>
</xsl:stylesheet>
